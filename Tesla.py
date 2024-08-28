from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
import requests
import plotly.graph_objects as go
from plotly.subplots import make_subplots

tesla = yf.Ticker("TSLA")

tesla_data = tesla.history(period='max')
tesla_data.reset_index(inplace=True)
print(tesla_data.head(5))

telsa_url = 'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm'
request = requests.get(url=telsa_url)
html_data = request.text

soup = BeautifulSoup(html_data, 'html.parser')

date_list = []
revenue_list = []
for row in soup.find_all('tbody')[1].find_all('tr'):
    col = row.find_all('td')
    if col != []:
        date = col[0].text
        revenue = col[1].text.replace('$','').replace(',','')
        date_list.append(date)
        revenue_list.append(revenue)

tesla_revenue_dict = {'Date':date_list, 'Revenue':revenue_list}

tesla_revenue = pd.DataFrame(tesla_revenue_dict)
tesla_revenue.dropna(inplace=True)
tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]

print(tesla_revenue.tail())
# tesla_revenue.to_csv('Tesla_yearly_revenue.xlsx', index=False)

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

make_graph(tesla_data, tesla_revenue, "Tesla")
