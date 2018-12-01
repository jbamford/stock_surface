"""
Author Jason Bamford
Date Nov 6th 2018
"""
import get_tickers as get_tickers
import back_test as back_test
import pandas as pd
import sample_slopes as sample_slopes
import numpy as np
import settings

def test_calculate_profit():
    """
    Makes sure that we can calculate the return if we just had held the stock
    """
    data = {
        'col4CLS': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4slope_sum': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.2, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4bid_stream': [None, None, None, None, None,1 , 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    stock_data = pd.DataFrame(data=data)

    print len(data['col4CLS'])
    print len(data['col4bid_stream'])

    # stock_data = pd.read_pickle('df_without_zeros.pkl')

    Back_Test = back_test.BackTest(
        stock_data, settings.settings_dict['test_model_path'])

    # def take_bid_stream_calculate_profit(self, column_bid_stream,
    # batch_size, look_ahead, for_graph=False):

    array_profit = Back_Test.take_bid_stream_calculate_profit(
        'col4bid_stream', 3, 2)
    print len(array_profit)

    array_of_nones = []
    for i in range(len(stock_data['col4bid_stream'].index) - len(array_profit)):
        array_of_nones.append(None)

    print len(stock_data['col4bid_stream'].index), ' len bid stream in df'
    print len(array_of_nones + array_profit)

    stock_data['profit'] = array_of_nones + array_profit

    stock_data.to_csv('files/testing_files/test-data.csv')

    # needed to round the answers bec python and floats 
    rounded_profits = []
    for number in array_profit:
        rounded_profits.append(round(number,1))

    assert rounded_profits == [0,0.3 ,0.1,0,0,0,0,0.1,0.3,-0.3,0,0,0,0, -0.4,0.3,-0.7,0.4,0.4,0.1]


def test_calculate_profit_all_ones():
    """
    Makes sure that we can calculate the return if we just had held the stock
    """
    data = {
        'col4CLS': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4slope_sum': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.2, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4bid_stream': [None, None, None, None, None,1 , 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    stock_data = pd.DataFrame(data=data)

    print len(data['col4CLS'])
    print len(data['col4bid_stream'])

    # stock_data = pd.read_pickle('df_without_zeros.pkl')

    Back_Test = back_test.BackTest(
        stock_data, settings.settings_dict['test_model_path'])

    # def take_bid_stream_calculate_profit(self, column_bid_stream,
    # batch_size, look_ahead, for_graph=False):

    array_profit = Back_Test.take_bid_stream_calculate_profit(
        'col4bid_stream', 3, 2)
    print len(array_profit)

    array_of_nones = []
    for i in range(len(stock_data['col4bid_stream'].index) - len(array_profit)):
        array_of_nones.append(None)

    print len(stock_data['col4bid_stream'].index), ' len bid stream in df'
    print len(array_of_nones + array_profit)

    stock_data['profit'] = array_of_nones + array_profit

    stock_data.to_csv('files/testing_files/test-data.csv')

    # needed to round the answers bec python and floats 
    rounded_profits = []
    for number in array_profit:
        rounded_profits.append(round(number,1))

    assert rounded_profits == [0,0.3 ,0.1,0.1,0.1,0.1,0.1,0.1,0.3,-0.3,0.5,0.1,-0.6,-0.1,-0.4,0.3,-0.7,0.4,0.4,0.1]


def test_calculate_profit_all_zeros():
    """
    Makes sure that we can calculate the return if we just had held the stock
    """
    data = {
        'col4CLS': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4slope_sum': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.2, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4bid_stream': [None, None, None, None, None,-1 , -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    }
    stock_data = pd.DataFrame(data=data)

    print len(data['col4CLS'])
    print len(data['col4bid_stream'])

    # stock_data = pd.read_pickle('df_without_zeros.pkl')

    Back_Test = back_test.BackTest(
        stock_data, settings.settings_dict['test_model_path'])

    # def take_bid_stream_calculate_profit(self, column_bid_stream,
    # batch_size, look_ahead, for_graph=False):

    array_profit = Back_Test.take_bid_stream_calculate_profit(
        'col4bid_stream', 3, 2)
    print len(array_profit)

    array_of_nones = []
    for i in range(len(stock_data['col4bid_stream'].index) - len(array_profit)):
        array_of_nones.append(None)

    print len(stock_data['col4bid_stream'].index), ' len bid stream in df'
    print len(array_of_nones + array_profit)

    stock_data['profit'] = array_of_nones + array_profit

    stock_data.to_csv('files/testing_files/test-data.csv')

    # needed to round the answers bec python and floats 
    rounded_profits = []
    for number in array_profit:
        rounded_profits.append(round(number,1))

    assert rounded_profits == [0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0, 0.0,0.0,0.0]

def test_calculate_profit_one_zero():
    """
    Makes sure that we can calculate the return if we just had held the stock
    """
    data = {
        'col4CLS': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4slope_sum': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.2, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4bid_stream': [None, None, None, None, None,1 , 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    stock_data = pd.DataFrame(data=data)

    print len(data['col4CLS'])
    print len(data['col4bid_stream'])

    # stock_data = pd.read_pickle('df_without_zeros.pkl')

    Back_Test = back_test.BackTest(
        stock_data, settings.settings_dict['test_model_path'])

    # def take_bid_stream_calculate_profit(self, column_bid_stream,
    # batch_size, look_ahead, for_graph=False):

    array_profit = Back_Test.take_bid_stream_calculate_profit(
        'col4bid_stream', 3, 2)
    print len(array_profit)

    array_of_nones = []
    for i in range(len(stock_data['col4bid_stream'].index) - len(array_profit)):
        array_of_nones.append(None)

    print len(stock_data['col4bid_stream'].index), ' len bid stream in df'
    print len(array_of_nones + array_profit)

    stock_data['profit'] = array_of_nones + array_profit

    stock_data.to_csv('files/testing_files/test-data.csv')

    # needed to round the answers bec python and floats 
    rounded_profits = []
    for number in array_profit:
        rounded_profits.append(round(number,1))

    assert rounded_profits == [0,0.3 ,0.1,0.1,0.1,0.1,0.1,0.1,0.3,-0.3,0,0,-0.6,-0.1,-0.4,0.3,-0.7,0.4,0.4,0.1]


def test_calculate_profit_two_consecutive_zero():
    """
    Makes sure that we can calculate the return if we just had held the stock
    """
    data = {
        'col4CLS': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4slope_sum': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.2, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4bid_stream': [None, None, None, None, None,1 , 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    stock_data = pd.DataFrame(data=data)

    print len(data['col4CLS'])
    print len(data['col4bid_stream'])

    # stock_data = pd.read_pickle('df_without_zeros.pkl')

    Back_Test = back_test.BackTest(
        stock_data, settings.settings_dict['test_model_path'])

    # def take_bid_stream_calculate_profit(self, column_bid_stream,
    # batch_size, look_ahead, for_graph=False):

    array_profit = Back_Test.take_bid_stream_calculate_profit(
        'col4bid_stream', 3, 2)
    print len(array_profit)

    array_of_nones = []
    for i in range(len(stock_data['col4bid_stream'].index) - len(array_profit)):
        array_of_nones.append(None)

    print len(stock_data['col4bid_stream'].index), ' len bid stream in df'
    print len(array_of_nones + array_profit)

    stock_data['profit'] = array_of_nones + array_profit

    stock_data.to_csv('files/testing_files/test-data.csv')

    # needed to round the answers bec python and floats 
    rounded_profits = []
    for number in array_profit:
        rounded_profits.append(round(number,1))

    assert rounded_profits == [0,0.3 ,0.1,0.1,0.1,0.1,0.1,0.1,0.3,0,0,.1,-0.6,-0.1,-0.4,0.3,-0.7,0.4,0.4,0.1]

def test_calculate_profit_long():
    """
    Makes sure that we can calculate the return if we just had held the stock
    """
    data = {
        'col4CLS': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1,1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1,1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1,1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4slope_sum': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.2, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1,1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1,1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1,1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4bid_stream': ['nan', 'nan', 'nan', 'nan', 'nan','nan' , 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 'nan', 1, 1, 1, 1, 1, 1,1,1,1,1,1 , 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1 , 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1,1,1,1,1 , 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    stock_data = pd.DataFrame(data=data)

    print len(data['col4CLS'])
    print len(data['col4bid_stream'])

    
    # stock_data = pd.read_pickle('df_without_zeros.pkl')


    Back_Test = back_test.BackTest(
        stock_data, settings.settings_dict['test_model_path'])

    # def take_bid_stream_calculate_profit(self, column_bid_stream,
    # batch_size, look_ahead, for_graph=False):

    array_profit = Back_Test.take_bid_stream_calculate_profit(
        'col4bid_stream', 18, 2)

    array_of_nones = []
    for i in range(len(stock_data['col4bid_stream'].index) - len(array_profit)):
        array_of_nones.append(None)

    # print len(stock_data['col4bid_stream'].index), ' len bid stream in df'
    # print len(array_of_nones + array_profit)

    stock_data['profit'] = array_of_nones + array_profit

    stock_data.to_csv('files/testing_files/test-data.csv')

    # needed to round the answers bec python and floats 
    rounded_profits = []
    for number in array_profit:
        rounded_profits.append(round(number,1))
    # print rounded_profits

    # assert rounded_profits == [0,0.3 ,0.1,0.1,0.1,0.1,0.1,0.1,0.3,0,0,.1,-0.6,-0.1,-0.4,0.3,-0.7,0.4,0.4,0.1]




def test_leads_with_none():
    """
    Makes sure that we can calculate the return if we just had held the stock
    """
    data = {
        'col4CLS': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4slope_sum': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.2, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4bid_stream': [None, None, None, None, None,1 , 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    stock_data = pd.DataFrame(data=data)

    print len(data['col4CLS'])
    print len(data['col4bid_stream'])

    # stock_data = pd.read_pickle('df_without_zeros.pkl')

    Back_Test = back_test.BackTest(
        stock_data, settings.settings_dict['test_model_path'])

    # def take_bid_stream_calculate_profit(self, column_bid_stream,
    # batch_size, look_ahead, for_graph=False):

    bid_streams = ['nan', 'nan', 'nan', 'nan', 'nan',1 , 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
    flag1 = Back_Test._validate_bid_stream_nones(bid_streams, 3,2)
    assert flag1 == True

    bid_streams = [1, 'nan', 'nan', 'nan', 'nan',1 , 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
    flag2 = Back_Test._validate_bid_stream_nones(bid_streams, 3,2)
    assert flag2 == False

    bid_streams = ['nan', 'nan', 'nan', 'nan', 1,1 , 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
    flag3 = Back_Test._validate_bid_stream_nones(bid_streams, 3,2)
    assert flag3 == False

    bid_streams = ['nan', 'nan', 'nan', 'nan', 'nan',1 , 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
    flag4 = Back_Test._validate_bid_stream_nones(bid_streams, 4,2)
    assert flag4 == False

    bid_streams = ['nan', 'nan', 'nan', 'nan', 'nan','nan' , 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
    flag5 = Back_Test._validate_bid_stream_nones(bid_streams, 4,2)
    assert flag5 == True
    
    bid_streams = ['nan', 'nan', 'nan', 'nan', 'nan','nan' , 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
    flag6 = Back_Test._validate_bid_stream_nones(bid_streams, 4,3)
    assert flag6 == False
        
    bid_streams = ['nan', 'nan', 'nan', 'nan', 'nan','nan' , 'nan', -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
    flag7 = Back_Test._validate_bid_stream_nones(bid_streams, 4,3)
    assert flag7 == True




def test_in_vallid_bid_stream():
    """
    Makes sure that we can calculate the return if we just had held the stock
    """
    data = {
        'col4CLS': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.1, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4slope_sum': [1, 1.2, 1.3, 1.7, 1.5, 1.2, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.4, 2.2, 2.6, 2.7, 2.1, 2.0, 1.6, 1.9, 1.2, 1.6, 2, 2.1],
        'col4bid_stream': [None, None, None, None, 1,1 , 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
    }
    stock_data = pd.DataFrame(data=data)

    print len(data['col4CLS'])
    print len(data['col4bid_stream'])

    # stock_data = pd.read_pickle('df_without_zeros.pkl')

    Back_Test = back_test.BackTest(
        stock_data, settings.settings_dict['test_model_path'])

    # def take_bid_stream_calculate_profit(self, column_bid_stream,
    # batch_size, look_ahead, for_graph=False):

    array_profit = Back_Test.take_bid_stream_calculate_profit(
        'col4bid_stream', 3, 2)

    assert array_profit == False