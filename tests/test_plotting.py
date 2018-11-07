"""
Author Jason Bamford
Date Aug 17 2018

"""
import get_tickers as get_tickers
import back_test as back_test
import pandas as pd
import sample_slopes as sample_slopes
import matplotlib.pyplot as plt
import numpy as np
import settings


def helper_turn_data_into_csv(stock_close, algo_proffits, bid_stream):
    """
    Takes a few arrays puts them all into a data frame and then ports that to a CSV to look at in excel
    """
    data_frame_for_csv = pd.DataFrame(
        {'stock_close': stock_close, 'algo_proffits': algo_proffits, 'bid_stream': bid_stream})
    data_frame_for_csv.to_csv('files/close_proffit_bid.csv')


def test_plot_stock():
    """
    Makes sure we can just plot a stock
    """
    ticker = 'GOOG'
    main_df = pd.read_pickle(settings.settings_dict['stock_data_path'])
    main_df = sample_slopes.create_slope_sum_market(main_df)

    Back_Test = back_test.BackTest(
        main_df, settings.settings_dict['model_path'])

    y_values = sample_slopes.generate_target_values(
        main_df, 18, ticker + 'CLS', 2)

    x_values = sample_slopes.create_batch_of_slopes(
        main_df, ticker + 'CLS', 18,   y_values[1])

    array_of_batches = Back_Test.create_batch_of_slopes(
        main_df, ticker + 'slope_sum', 18, y_values[1])

    Back_Test.append_list_of_buy_sells(array_of_batches,
                                       ticker + "slope_sum")

    algorithm_return = Back_Test.take_bid_stream_calculate_profit(
        ticker + "bid_stream", 18, 2, for_graph=True)

    array_of_bid_stream = Back_Test.main_df[ticker + 'bid_stream'].tolist()
    index_bid_stream = range(0, len(array_of_bid_stream))

    array_of_bid_stream = np.array(array_of_bid_stream) * 5

    runningTotal = []
    total = 0
    for n in algorithm_return:
        total += n
        runningTotal.append(total)

    # list_of_bids = Back_Test.array_of_profits
    index = range(0, len(runningTotal))

    index_stock = range(0, len(main_df[ticker + 'CLS'].tolist()))

    plt.plot(index_stock, main_df[ticker + 'CLS'].tolist(), 'r')

    plt.plot(index, runningTotal, 'g')

    plt.title(ticker + ' Profit')

    plt.plot(index_bid_stream, array_of_bid_stream, 'b')

    print len(main_df[ticker + 'CLS'].tolist()), 'length of the close valeus'
    print len(algorithm_return), 'algo proffits'
    print len(runningTotal), 'runnign total'
    print len(array_of_bid_stream), 'bid stream len'
    print array_of_bid_stream[:50], 'bid stream'

    helper_turn_data_into_csv(
        main_df[ticker + 'CLS'].tolist()[:len(runningTotal)], runningTotal, array_of_bid_stream[:len(runningTotal)])

    plt.show()

    # TODO make sure that the running total account for weather or not we have a hold
    # at the end of the time sequance the stock should track if we have a hold

if __name__ == '__main__':
    test_plot_stock()
