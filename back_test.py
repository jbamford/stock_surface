"""
Author: Jason BAmford
Date: 7/29/18
"""

from sklearn.externals import joblib
import pandas as pd
import numpy as np


class BackTest():
    """
    This back testing class is used to handle the checking to see if the alorith works

    it takes a datafram of all the differnt stocks and stockslopes

    """

    def __init__(self, data_frame, path_of_model):
        self.main_df = data_frame
        self.model = joblib.load(path_of_model)

    def batch_sample_slopes(self):
        """
        used to take in the sample slopes
        """
        pass

    def _sliding_window(self, sequence, winSize, step=1):
        """Returns a generator that will iterate through
        the defined chunks of input sequence.  Input sequence
        must be iterable."""

        # Pre-compute number of chunks to emit
        numOfChunks = ((len(sequence) - winSize) / step) + 1

        # Do the work
        for i in range(0, numOfChunks * step, step):
            yield sequence[i:i + winSize]

    def create_batch_of_slopes(self, df, column_with_slope_sum, batch_count, cut_length):
        """
        Takes a dataframe of closes changes and slopes and creates batches of the slopes of size batch_count
        """

        # take the dataframe makes it a list. Then only takes the front part of
        # it and sends it to the sliding window to get the featchure chunks
        list_of_chunks = list(self._sliding_window(
            df[column_with_slope_sum].tolist(), batch_count))

        return list_of_chunks[:cut_length]

    def generate_buy_sells(self, batch):
        """
        This function takes batches of slope sums and applys that to the model it returns 1 or 0
        """
        return self.model.predict([batch])

    def append_list_of_buy_sells(self, list_of_batches, column_name):
        """
        Takes a list of batches and makes a new column in the self.main_df
        that will store the differnt values 0/1
        """
        array_of_buy_sells = []
        for batch in list_of_batches:
            should_buy_or_sell = self.generate_buy_sells(batch)
            # print should_buy_or_sell, ' should buy sell'
            array_of_buy_sells.append(int(should_buy_or_sell))

        # print array_of_buy_sells, ' here is buy sells'
        # print pd.Series(array_of_buy_sells), ' here is serreis of same '
        # print len(self.main_df), 'lenght of the datafram'
        # print len(array_of_buy_sells), ' len of the bid stream'

        # makes sure that the two arrays match each other when they are added
        # together

        array_of_nones = []
        for i in range(len(self.main_df) - len(array_of_buy_sells)):
            array_of_nones.append(None)

            # NOTE
            # needed to add the nones to the begining of the buy_sell array since
            # it starts caculating weatther or not to buy or sell a few days
            # into the close values

        # remove the last bid
        del array_of_buy_sells[-1]
        array_of_nones.append(None)

        self.main_df[column_name.replace(
            'slope_sum', 'bid_stream')] = array_of_nones + array_of_buy_sells

        return self.main_df

    def log_return(self, finial, initial):
        """
        Takes two number and caculates there log return
        """
        return np.log(float(finial) / float(initial))

    def percent_change(self, finial, initial):
        """
        Takes two number and caculates there log return
        """
        return (float(finial) - float(initial) / float(initial))

    def test_calculate_holding_log_return(self, column_with_close):
        """
        This function takes a column with a close and caculates its return if someone just held the stock
        and then sold it at the end of the testing period
        """
        array_of_closes = self.main_df[column_with_close].tolist()

        array_of_returns = []
        i = 0

        while i < len(array_of_closes) - 1:
            array_of_returns.append(
                self.log_return(array_of_closes[1 + int(i)], array_of_closes[i]))

            i += 1

        return array_of_returns

    def calculate_holding_percent_change_return(self, column_with_close):
        """
        Uses the common formula of percent change
        """
        array_of_closes = self.main_df[column_with_close].tolist()

        return (float(array_of_closes[-1]) - float(array_of_closes[0])) / float(array_of_closes[0])

    def calculate_holding_profit(self, column_with_close, batch_size, look_ahead):
        """
        Uses the common formula of percent change
        """
        # need to shift the column in order to not count hte first few days bec there wasnt any data to make
        # a buy or sell claim
        array_of_closes = self.main_df[column_with_close].tolist()[
            (batch_size + look_ahead):]

        return float(array_of_closes[-1]) - float(array_of_closes[0])

    def take_bid_stream_calculate_return(self, column_bid_stream, batch_size, look_ahead):
        """
        This function take a column with a bid stream then reads the bid stream
        then looks at the corospoiding close prices and caculates our return
        """
        array_of_bid_stream = self.main_df[
            column_bid_stream].tolist()

        array_of_closes = self.main_df[
            column_bid_stream.replace('bid_stream', "CLS")].tolist()

        index = 0

        buy_price = 0
        sell_price = 0
        holding = 0

        self.array_of_returns = []

        print array_of_bid_stream, 'array of bid stream'

        for bid in array_of_bid_stream:
            try:
                bid = int(bid)
            except:
                print "failsed here"
                return self.array_of_returns

            if bid == 1 and holding == 0:
                # will only happen in the first case and after a 0

                # set the price at the current index to the new buy_price
                buy_price = array_of_closes[index]

                self.array_of_returns.append(0)

                holding = 1

            if bid == -1 and holding != 0:
                # cannot happen the first time bec it starts at a 0
                # this is when we should sell the stock after a bunch of 1's

                try:
                    sell_price = array_of_closes[
                        index + batch_size + look_ahead]
                except:
                    print "failsed heres"
                    return self.array_of_returns
                # now its time to sell out and calc return
                self.array_of_returns.append(
                    self.percent_change(sell_price, buy_price))

                holding = 0

            if bid == 1 and holding == 1:
                # this is when the buy price was already set and we need to
                # keep movin on

                self.array_of_returns.append(0)
                holding = 1

            if bid == -1 and holding == 0:

                self.array_of_returns.append(0)
                holding = 0

            if bid == None:
                print "the bid was  none"
                return self.array_of_returns

            print "bid: {} - buy_price: {} - sell_price: {} - holding: {}".format(str(bid), str(buy_price), str(sell_price), str(holding))

            # TODO should return data frame not array
            index += 1

        return self.array_of_returns

    def check_if_prior_days_have_a_buy_signal(self, array_of_bid_stream, array_of_closes, index):
        """
        this function takes the bid and closes arrays with an index to check

        it will return the close price if the index for the day in the bid stream is in fact a 1

        """
        bid = array_of_bid_stream[index]
        if bid == 1:
            return True, array_of_closes[index]
        else:
            return False, 0

    def _validate_bid_stream_nones(self, bid_stream, batch_size, look_ahead):
        """
        This helper method is used to validate that the incoming bid stream has the first initial Nones equal to the batchsize + look ahead
        returns True or False
        """
        print bid_stream, 'bid stream '
        for value in bid_stream[:batch_size + look_ahead]:
            print value
            if str(value) != 'nan':
                return False
        return True

    def take_bid_stream_calculate_profit(self, column_bid_stream, batch_size, look_ahead, for_graph=False):
        """
        This function take a column with a bid stream then reads the bid stream
        then looks at the corospoiding close prices and caculates our return
        """
        array_of_bid_stream = self.main_df[
            column_bid_stream].tolist()[batch_size + look_ahead:]

        print array_of_bid_stream, ' here is bid from fucntion'
        # print len(array_of_bid_stream), 'array of bid streams in the
        # back_test.py'

        array_of_closes = self.main_df[
            column_bid_stream.replace('bid_stream', "CLS")].tolist()[batch_size + look_ahead:]

        # this is when the function got a bid stream that didnt start with the
        # right amount of Nones for the offset
        if not self._validate_bid_stream_nones(self.main_df[column_bid_stream].tolist(), batch_size, look_ahead):
            return False

        index = 0
        buy_price = 0
        sell_price = 0
        holding = 0

        appended_first_price = False

        self.array_of_profits = []
        if array_of_bid_stream[0] == 1:
            if for_graph == True:
                self.array_of_profits.append(array_of_closes[0])
                appended_first_price = True

        while index < len(array_of_bid_stream):
            # print bid , ' bid',  array_of_closes[index] , ' close',
            # buy_price, ' buy price' ,sell_price , ' sell price' ,
            try:
                bid = int(array_of_bid_stream[index])
                print "index {} | bid {} | holding {} | close {} | buy_price {} | sell_price {}".format(str(index), str(bid), str(holding), str(array_of_closes[index]), str(buy_price), str(sell_price))

            except:
                print "it failed on NONE Value"
                if holding == 1:
                    self.array_of_profits.append(
                        array_of_closes[index] - buy_price)
                return self.array_of_profits

            if bid == 1 and holding == 0:
                # will only happen in the first case and after a 0

                if not appended_first_price:
                    if for_graph == True:
                        self.array_of_profits.append(array_of_closes[index])

                # set the price at the current index to the new buy_price
                buy_price = array_of_closes[index]

                self.array_of_profits.append(0)

                holding = 1

            elif bid == -1 and holding == 1:
                # cannot happen the first time bec it starts at a 0
                # this is when we should sell the stock after a bunch of 1's

                is_there_a_one, close_value = self.check_if_prior_days_have_a_buy_signal(
                    array_of_bid_stream, array_of_closes, index - 1)

                while not is_there_a_one:
                    index = index - 1
                    is_there_a_one, close_value = self.check_if_prior_days_have_a_buy_signal(
                        array_of_bid_stream, array_of_closes, index)

                buy_price = close_value

                sell_price = array_of_closes[
                    index]
                # except:
                #     print "failsed trying to look ahead"

                # if holding == 1:
                #     self.array_of_profits.append(
                #         array_of_closes[index] - buy_price)

                # return self.array_of_profits
                # now its time to sell out and calc return

                # we dont want it to check the stock inbween the look ahead day and the day we got the sell signal
                # were just going to hold out and append 0 until we sell
                print 'jason here si the sell price', sell_price
                self.array_of_profits.append(sell_price - buy_price)
                # print 'gettign to the for statment'
                for _ in range(look_ahead - 1):
                    # print "it should add a 0"
                    self.array_of_profits.append(0.000000001)

                # bump the index up by the look_ahead amount to start the next
                # incoming bid to the correct day
                index = index + look_ahead - 1
                holding = 0
                buy_price = 0
                sell_price = 0

            elif bid == 1 and holding == 1:
                # this is when the buy price was already set and we need to
                # keep movin on

                self.array_of_profits.append(
                    array_of_closes[index] - array_of_closes[index - 1])

                # if caculating the proffit over time it shouldn't keep adding
                # priovious day

                holding = 1

            elif bid == -1 and holding == 0:
                # shift up the index bec we dont want to buy anything if we
                # know the stock will go down in the amount of look_ahead days
                # if index < len(array_of_bid_stream) - (look_ahead):
                print "index was less"
                index = index + look_ahead - 1

                self.array_of_profits.append(0)

                for _ in range(look_ahead - 1):
                        # print "it should add a 0"
                    self.array_of_profits.append(0.000000001)
                holding = 0
                # else:
                #     print "index was more"
                #     return self.array_of_profits

            elif bid == None:
                print "the bid was none"

                if holding == 1:
                    self.array_of_profits.append(
                        array_of_closes[index] - buy_price)
                return self.array_of_profits

            # print "bid: {} - buy_price: {} - sell_price: {} - holding:
            # {}".format(str(bid), str(buy_price), str(sell_price),
            # str(holding))

            # TODO should return data frame not array
            index += 1

        return self.array_of_profits
