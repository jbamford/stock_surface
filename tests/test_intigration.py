import pytest
import sample_slopes as sample_slopes
import support_vector as support_vector
import numpy as np
import pandas as pd


def test_train_on_test_data():

    data = {'col1CLS': [3, 3, 4, 5, 7, 8, 7, 6, 5, 4],
            'col2CLS': [6, 5, 5, 6, 7, 6, 4, 3, 3, 8],
            'col3CLS': [7, 6, 4, 6, 4, 2, 4, 5, 6, 5],
            'col4CLS': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col5CLS': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col1CHG': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col2CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col3CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col4CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col5CHG': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col2slope_sum': [13, 8, -3, 3, 3, 3, 3, 3, 3, 3],
            'col3slope_sum': [1, -3, 3, 5, 3, 3, 3, 3, 3, 3],
            'col4slope_sum': [9, 3, 9, 3, -3, 7, -14, 3, 99, 3],
            }
    stock_data = pd.DataFrame(data=data)

    # generate_target_values(df, batch_count, column_name, look_ahead)
    y_values = sample_slopes.generate_target_values(
        stock_data, 3, 'col2CLS', 2)

    # create_batch_of_slopes(df, batch_count, cut_length)
    x_vaules = sample_slopes.create_batch_of_slopes(
        stock_data, 'col2slope_sum', 3,   y_values[1])

    print x_vaules, 'x values'
    print y_values[0], ' yvalues'

    sv = support_vector.Support_Vector(x_vaules, y_values[0])
    sv.train()
    assert sv.predict_out_put([[-0.8, -1, 0]]) == [0]


def test_iterate_and_persist_slope_sums():
    """
    used to make sure that i can make the logic to maintain the congruency between
    featcures and targetvalues across all slope_sum_cols
    """

    data = {'col1CLS': [3, 3, 4, 5, 7, 8, 7, 6, 5, 4],
            'col2CLS': [6, 5, 5, 6, 7, 6, 4, 3, 3, 8],
            'col3CLS': [7, 6, 4, 6, 4, 2, 4, 5, 6, 5],
            'col4CLS': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col5CLS': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col1CHG': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            'col2CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col3CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col4CHG': [4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
            'col5CHG': [3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            'col2slope_sum': [13, 8, -3, 3, 3, 3, 3, 3, 3, 3],
            'col3slope_sum': [1, -3, 3, 5, 3, 3, 3, 3, 3, 3],
            'col4slope_sum': [9, 3, 9, 3, -3, 7, -14, 3, 99, 3],
            }
    stock_data = pd.DataFrame(data=data)

    columns = list(stock_data)

    columns_with_sample_slopes = sample_slopes.get_columns_with_slope_sum(
        columns)

    sv = support_vector.Support_Vector([], [])

    for column in columns_with_sample_slopes:

        y_values = sample_slopes.generate_target_values(
            stock_data, 3, column.replace('slope_sum', 'CLS'), 2)
        sv.Y = sv.Y + y_values[0]

        # create_batch_of_slopes(df, batch_count, cut_length)
        # y_values[1] bec thats used to tell create batch_of_slopes where to
        # stop
        x_values = sample_slopes.create_batch_of_slopes(
            stock_data, column, 3,   y_values[1])

        sv.X = sv.X + x_values

    print sv.X, 'xvalues'
    print sv.Y, 'yvalues'
    sv.train()
    assert sv.predict_out_put([[9, 3, -3]]) == [1]

    test_data = [[1.00893849384939849, 2, 3], [9, 3, -3], [-1, 5, 3],
                 [8, -3, 3], [-3, 3, 3], [3, 3, 3], [3, 3, 3], ]
    for sample in test_data:
        print sv.predict_out_put([sample])
