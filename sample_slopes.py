import numpy as np
import pandas as pd


def create_slope_sum(df):
    """
    Takes a dataframe and looks at all the columns with perfecnt change. Then looks to the left and right
    of each chnagne column and sums the left and right.

    returns the oringal dataframe with the new columns called Slope_sum
    """

    columns = df.columns

    # filter the columns with CHG vs CLS
    CLS_columns, CHG_columns = get_columns_with_CLS(columns)

    # get rid of the CLS columns and only run slop on the CHG columns
    droped_df = df.drop(columns=CLS_columns)

    column_index = 1

    while column_index < len(CHG_columns) - 1:

        # caculate the slope between L & R columns then sum them
        slope_sum = df[CHG_columns[column_index]] - df[CHG_columns[column_index - 1]] + \
            df[CHG_columns[column_index]] - df[CHG_columns[column_index + 1]]

        # add the newly formed column containing the slope info to the main df
        df[str(CHG_columns[column_index].replace('CHG', 'slope_sum'))] = slope_sum

        column_index += 1

    return df


def create_slope_sum_market(df):
    """
    Takes a dataframe and looks at all the columns with perfecnt change. Then it compairs the stock of intreste and caculates
    the differnce between it and the rest of the percent changes on that day in the market. Finally it sums them up.

    returns the oringal dataframe with the new columns called Slope_sum
    """

    columns = df.columns

    # filter the columns with CHG vs CLS
    CLS_columns, CHG_columns = get_columns_with_CLS(columns)

    # print CHG_columns, ' chagne columns'

    column_index = 1

    while column_index < len(CHG_columns) - 1:

        stock_looking_at = CHG_columns[column_index]

        # make dataframe of a bunch of zeros to the size of the df coming in
        slope_sum = pd.DataFrame(np.zeros((len(df.index), 1)))

        for stock in CHG_columns:

            if stock != stock_looking_at:

                slope_sum[0] = slope_sum[0] + \
                    df[CHG_columns[column_index]] - df[stock]

        # add the newly formed column containing the slope info to the main df
        df[str(CHG_columns[column_index].replace('CHG', 'slope_sum'))] = slope_sum

        column_index += 1
    # print df
    return df


def get_columns_with_CLS(columns):
    """
    Takes an array of columns and returns the ones with CLS at the end
    """

    columns_with_CLS = []
    CHG_columns = []
    for column in columns:

        # look at the last 3 characters
        if column[-3:] == 'CLS':
            columns_with_CLS.append(column)
        else:
            CHG_columns.append(column)
    return columns_with_CLS, CHG_columns


def get_columns_with_slope_sum(columns):
    """
    Takes an array of columns and returns the ones with slope_sum at the end
    """

    columns_with_slope_sum = []
    for column in columns:
        # look at the last 9 characters
        if column[-9:] == 'slope_sum':
            columns_with_slope_sum.append(column)
    return columns_with_slope_sum


def _sliding_window(sequence, winSize, step=1):
    """Returns a generator that will iterate through
    the defined chunks of input sequence.  Input sequence
    must be iterable."""

    # Pre-compute number of chunks to emit
    numOfChunks = ((len(sequence) - winSize) / step) + 1

    # Do the work
    for i in range(0, numOfChunks * step, step):
        yield sequence[i:i + winSize]


def generate_target_values(df, batch_count, column_name, look_ahead):
    """
    Takes a dataframe and a batch count to gernate the % change values good or bad for each batch
    """

    list_of_closes = df[column_name].tolist()

    i = 0
    target_values = []
    while i < (len(list_of_closes) - (look_ahead + batch_count) + 1):

        target_day_index = i + batch_count + look_ahead - 1

        percent_change = find_percent_change(
            list_of_closes[target_day_index], list_of_closes[i + batch_count - 1])

        if percent_change < 0:
            target_values.append(-1)
        else:
            target_values.append(1)
        i += 1
    number_of_target_values = len(target_values)

    return target_values, number_of_target_values


def find_percent_change(new_number, old_number):
    """
    takes two numbers returns percent change

    """

    # return np.log(float(new_number) / float(old_number))
    return (float(new_number) - float(old_number)) / float(old_number)


def create_batch_of_slopes(df, column_with_slope_sum, batch_count, cut_length):
    """
    Takes a dataframe of closes changes and slopes and creates batches of the slopes of size batch_count
    """

    # take the dataframe makes it a list. Then only takes the front part of
    # it and sends it to the sliding window to get the featchure chunks
    list_of_chunks = list(_sliding_window(
        df[column_with_slope_sum].tolist(), batch_count))

    return list_of_chunks[:cut_length]


def moving_average(a, n):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def create_batch_of_slopes_moving_av(df, column_with_slope_sum, batch_count, cut_length, moving_window):
    """
    Takes a dataframe of closes changes and slopes and creates batches of the slopes of size batch_count
    """

    # take the dataframe makes it a list. Then only takes the front part of
    # it and sends it to the sliding window to get the featchure chunks
    list_of_chunks = list(_sliding_window(
        df[column_with_slope_sum].tolist(), batch_count))

    moving_av_chunks = []
    for chunk in list_of_chunks:
        moving_av_chunks.append(moving_average(chunk, moving_window))

    return moving_av_chunks[:cut_length]
