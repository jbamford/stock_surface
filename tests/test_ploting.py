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


def test_plot_stock():
    """
    Makes sure we can just plot a stock
    """
    ticker = 'GOOG'
    main_df = pd.read_pickle('df_without_zeros.pkl')
    main_df = sample_slopes.create_slope_sum(main_df)

    Back_Test = back_test.BackTest(
        main_df, '/Users/jasonbamford/workspace/stock_surface/model_18_batch.pkl')

    y_values = sample_slopes.generate_target_values(
        main_df, 18, ticker + 'CLS', 2)

    x_values = sample_slopes.create_batch_of_slopes(
        main_df, ticker + 'CLS', 18,   y_values[1])

    array_of_batches = Back_Test.create_batch_of_slopes(
        main_df, ticker + 'slope_sum', 18, y_values[1])

    Back_Test.append_list_of_buy_sells(array_of_batches,
                                       ticker + "slope_sum")

    algorithm_return = Back_Test.take_bid_stream_calculate_profit(
        ticker + "bid_stream", 18, 2)

    runningTotal = []

    total = 0
    print algorithm_return, 'algo return'
    for n in algorithm_return:
        total += n
        runningTotal.append(total)

    print runningTotal, 'cum sum'
    # list_of_bids = Back_Test.array_of_profits
    index = range(0, len(runningTotal))

    index_stock = range(0, len(main_df[ticker + 'CLS'].tolist()))

    plt.plot(index_stock, main_df[ticker + 'CLS'].tolist(), 'r')

    plt.plot(index, runningTotal, 'g')

    plt.show()

    # TODO make sure that the running total account for weather or not we have a hold
    # at the end of the time sequance the stock should track if we have a hold
