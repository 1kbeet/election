import altair as alt
import streamlit as st
from PIL import Image
import requests
import pandas as pd

alt.data_transformers.disable_max_rows()
#image = Image.open(r"C:\\Users\\bradl\\Pictures\\beetle.png")

st.set_page_config(
    page_title="Beetle",
    layout="wide",
)
c1, c2 = st.columns([1, 3])

c2.header("AIP-183 Voting")
c2.caption(
    """
    A deep dive on Royalty Data from Ethereum Network. Powered by [Flipside Crypto](https://flipsidecrypto.xyz/)
    
    Twitter: [@1kbeetlejuice](https://twitter.com/1kbeetlejuice) 
    """
)
#c1.image(
#    image,
#    width=100,
#)


# Set the GraphQL endpoint URL
url = 'https://hub.snapshot.org/graphql?operationName=Votes&query=query%20Votes%20%7B%0A%20%20votes%20(%0A%20%20%20%20first%3A%20100%0A%20%20%20%20skip%3A%200%0A%20%20%20%20where%3A%20%7B%0A%20%20%20%20%20%20proposal%3A%20%220x2485aa565a28902bd33bbba1f91e9c7b66cf34010bd25c4bef82cd8e341071d8%22%0A%20%20%20%20%7D%0A%20%20%20%20orderBy%3A%20%22vp%22%2C%0A%20%20%20%20orderDirection%3A%20desc%0A%20%20)%20%7B%0A%20%20%20%20voter%0A%20%20%20%20choice%0A%20%20%20%20vp%0A%20%20%7D%0A%7D%0A'

# Set the GraphQL query
query = '''
query Votes {
  votes (
    first: 1000
    skip: 0
    where: {
      proposal: "0x2485aa565a28902bd33bbba1f91e9c7b66cf34010bd25c4bef82cd8e341071d8"
    }
    orderBy: "vp",
    orderDirection: desc
  ) {
    voter
    choice
    vp
  }
}
'''

# Set the GraphQL variables (if any)
variables = {}

# Set the request headers
headers = {'Content-Type': 'application/json'}

# Make the GraphQL request
response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

# Get the data from the response
data = response.json()['data']['votes']

# Convert the data to a Pandas DataFrame
df = pd.DataFrame(data)

# Calculate the sum of the 'vp' column
vp_sum = df['vp'].sum()

# Display the sum as a large text box with a title
st.markdown(f'<h1 style="font-size:50px">Total Voting Power: {vp_sum:,.2f}</h1>', unsafe_allow_html=True)

# Convert the 'vp' column values to floats
df['vp'] = df['vp'].apply(lambda x: float(x))

# Convert the 'vp' column values to floats and handle invalid values
def convert_to_float(x):
  try:
    return float(x)
  except ValueError:
    return 0

df['vp'] = df['vp'].apply(convert_to_float)

# Add a new column to the DataFrame for the formatted 'vp' values
df['vp'] = df['vp'].apply(lambda x: '{:,.2f}'.format(x))

# Add a new column to the DataFrame for the 'choice' values
df['choice'] = df['choice'].apply(lambda x: 'In Favor' if x == 1 else 'Against')

# Calculate the total sum of the 'vp' column
vp_total = df['vp'].sum()

# Add a new column to the DataFrame for the 'vp' values as a percentage of the total
#df['vp_percent'] = df['vp'].apply(lambda x: (x / vp_total) * 100)
#df['vp_percent'] = df['vp_percent'].apply(convert_to_float)

# Display the table
st.table(df)

