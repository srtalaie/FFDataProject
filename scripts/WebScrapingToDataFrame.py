import pandas as pd
from bs4 import BeautifulSoup as BS
import requests

URL = 'https://www.fantasyfootballdatapros.com/table'

res = requests.get(URL)

if res.ok:
    print('Response was OK!')

soup = BS(res.content, 'html.parser')

table = soup.find('table')

#You can read more about pandas.DataFrame.read_html here
#https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_html.html

df = pd.read_html(str(table))[0]

# remove the first column on our dataframe. It's an unneccessary index column
df = df.iloc[:, 1:]

df.head()