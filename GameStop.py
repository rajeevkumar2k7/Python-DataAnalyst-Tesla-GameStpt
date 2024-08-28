from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

game_stop = yf.Ticker('GME')
game_data = game_stop.history(period='max')
game_data.reset_index(inplace=True)
print(game_data.head())

url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html'
htm_data_2 = requests.get(url).text

soup = BeautifulSoup(htm_data_2, 'html.parser')

columns = ['Date','Revenue']
gme_revenue = pd.DataFrame(columns=columns)

for row in soup.find_all('tbody')[1].find_all('tr'): 
    col = row.find_all('td')
    if col != []:
        date = col[0].text
        revenue = col[1].text.replace(",",'').replace("$",'')
        gme_revenue = gme_revenue._append({'Date':date, 'Revenue':revenue}, ignore_index = True)

print(gme_revenue.tail())

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

make_graph(game_data, gme_revenue, "GameStop")
