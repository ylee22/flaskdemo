from flask import Flask, render_template, request, redirect
import pandas_datareader.data as web
import pandas as pd
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
import os

app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    # ask for stock ticker
    if request.method == 'GET':
        return render_template('stockinfo.html')
    else:
        # request was a POST, which means user gave stock ticker
        ticker = request.form['stocktick']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        stockinfo = stock(ticker, startdate, enddate)
        closing = stockinfo.close
        dates = pd.to_datetime(stockinfo.index)

        # plot using bokeh
        # create a new plot with a datetime axis type
        p = figure(title=ticker, x_axis_label='date', y_axis_label='closing price', x_axis_type='datetime')
        p.line(dates, closing, line_width=2)

        # save
        html = file_html(p, CDN, "stock closing price")

        f = open('templates/test.html', 'w')
        f.write(html)
        f.close()

        return render_template('test.html')


# function for getting stock prices for a given company
def stock(symbol, start, end):
    # get the stock
    # start and end are dates in string (year-month-date)
    f = web.DataReader(symbol, 'iex', start, end)
    return f

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
