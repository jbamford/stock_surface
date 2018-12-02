# Stock Surface - Machine Learning Algorithm To Predict Stock Direction

This module was motivated by a [unique feature](https://medium.com/p/d54b7666cc7c/) set I wanted to test. 


## Installation


```bash
git clone [repository]
```

## Useful Files

__get_tickers.py__

This is the main function that pulls the stock data manipulates the feature set and trains the model. 

__sample_slopes.py__

This file holds the functions to perform the feature and target value manipulation on the stock data.

__settings.py__

Holds the settings for the backtesting

__support_vector.py___

This holds the class that's used for ML

__plotly_web.py__

Used for making a pretty 3D surface graph on Plotly

__tests/test_plotting.py__
Used for inputting a stock ticker and having it make a graph of the algorithm's returns alongside the close prices and trade indicators. 

__tests/test_back_test.py__

These functions are used to test how well your model did on the market data most notably: test_on_array_of_tickers_profit() 

This will output a CSV file that you can compare how each stock did to just holding it. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)