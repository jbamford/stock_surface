"""
Author Jason Bamford
Date Sep 9th 2018

"""
import get_tickers as get_tickers
import back_test as back_test
import pandas as pd
import sample_slopes as sample_slopes
import matplotlib.pyplot as plt
import numpy as np

from statsmodels import regression
import statsmodels.api as sm
import math
import seaborn
from statsmodels.stats.stattools import jarque_bera
from statsmodels import regression, stats
import settings


def linreg(X, Y):
    """
    need to look at Prob (F-statistic): make sure its <.05 for significgance
    """
    # Running the linear regression

    X = sm.add_constant(X)
    model = regression.linear_model.OLS(Y, X).fit()
    a = model.params[0]
    b = model.params[1]
    X = X[:, 1]

    # Return summary of the regression and plot results
    X2 = np.linspace(X.min(), X.max(), 100)
    Y_hat = X2 * b + a
    # plt.scatter(X, Y, alpha=0.3)  # Plot the raw data
    # Add the regression line, colored in red
    plt.plot(X2, Y_hat, 'r', alpha=0.9)
    plt.xlabel('X Value')
    plt.ylabel('Y Value')
    plt.show()
    return model.summary()


def test_variance_of_slope_sums():
    """
    Used to check the variance of the values formt he slopesum
    """

    ticker = 'GOOG'
    main_df = pd.read_pickle(settings.settings_dict['stock_data_path'])

    main_df = sample_slopes.create_slope_sum(main_df)

    slope_sums = main_df[ticker + "slope_sum"]

    print np.mean(main_df[ticker + "slope_sum"])
    print np.std(main_df[ticker + "slope_sum"])

    std = pd.rolling_std(slope_sums, window=20)

    _, ax2 = plt.subplots()

    ax2.plot(slope_sums)
    ax2.plot(slope_sums + std)
    ax2.plot(slope_sums - std)
    plt.legend(['Slope_Sum ', 'Slope_Sum +1 Std', 'Slope_Sum -1 Std'])
    plt.title(ticker + ' varrience of slope sum')
    plt.show()


def test_slope_sum_stock_price():
    """
    Used to check the variance of the values formt he slopesum
    makes sure the slope sum is normially distribueted
    """

    ticker = 'FB'
    main_df = pd.read_pickle(settings.settings_dict['stock_data_path'])
    main_df = sample_slopes.create_slope_sum(main_df)

    slope_sums = main_df[ticker + "slope_sum"]

    print np.mean(main_df[ticker + "slope_sum"])
    print np.std(main_df[ticker + "slope_sum"])

    # test for normality
    assert jarque_bera(main_df[ticker + "slope_sum"])[1] < .005

    # std = pd.rolling_std(slope_sums, window=20)

    plt.figure(1)

    plt.subplot(211)
    plt.plot(main_df[ticker + "CLS"])

    plt.title(str(ticker) + ' Price and Slope Sum')

    plt.subplot(212)
    plt.plot(slope_sums)

    plt.show()


def test_correlation_of_variance_and_returns():
    """
    Need to run tests/test_back_test::test_on_array_of_tickers_profit in order to genrate a
    dataframe of stat values

    # NOTE high varirent slope_sums returns more proffit
    """
    meaningful_stats = pd.read_pickle(
        'files/meaningfull_stats.pkl')

    print meaningful_stats
    print linreg(meaningful_stats['std'].tolist(),
                 meaningful_stats['returns_diff'].tolist())


def test_regression_of_slope_sum_distribution():
    """
    uses the seaborn package to visulize the distribution for the slopesums
    """

    meaningful_stats = pd.read_pickle(
        'files/meaningfull_stats.pkl')

    print meaningful_stats['std'].tolist()
    print meaningful_stats['returns_diff'].tolist()

    def make_float(array):
        """
        takes an array and makes all the number in it floats
        """
        finial_array = []

        for number in array:
            finial_array.append(float(number))
        return finial_array

    seaborn.regplot(meaningful_stats['std'], meaningful_stats['returns_diff'])

    plt.title("STD and Returns")

    plt.axhline(y=00, color='r', linestyle='-')

    plt.show()
