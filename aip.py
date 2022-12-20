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

c2.header("ApeCoin DAO – Special Council Nominees - Term Beginning January 2023")
c2.caption(
    """
    ApeCoin DAO voting results, sorted by newest to oldest. working on fixing choices column.
    
    Twitter: [@1kbeetlejuice](https://twitter.com/1kbeetlejuice) 
    """
)
#c1.image(
#    image,
#    width=100,
#)


# Set the GraphQL endpoint URL
url = 'https://hub.snapshot.org/graphql?operationName=Votes&query=query%20Votes%20%7B%0A%20%20votes%20(%0A%20%20%20%20first%3A%201000%0A%20%20%20%20skip%3A%200%0A%20%20%20%20where%3A%20%7B%0A%20%20%20%20%20%20proposal%3A%20%220x2485aa565a28902bd33bbba1f91e9c7b66cf34010bd25c4bef82cd8e341071d8%22%0A%20%20%20%20%7D%0A%20%20%20%20orderBy%3A%20%22vp%22%2C%0A%20%20%20%20orderDirection%3A%20desc%0A%20%20)%20%7B%0A%20%20%20%20created%0A%20%20%20%20voter%0A%20%20%20%20choice%0A%20%20%20%20vp%0A%20%20%7D%0A%7D%0A'
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
    created
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


# Group the DataFrame by the 'choices' column and calculate the sum of the 'vp' column for each group
df_grouped = df.groupby('choices')['vp'].sum().reset_index()

# Create the pie chart
chart = alt.Chart(df_grouped).mark_arc().encode(
    x='vp',
    y='choice',
    color='choice',
    startAngle=0,
    endAngle=360
)

# Display the chart
st.altair_chart(chart)

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

# Calculate the total sum of the 'vp' column
vp_total = df['vp'].sum()

# Add a new column to the DataFrame for the 'vp' values as a percentage of the total
#df['vp_percent'] = df['vp'].apply(lambda x: (x / vp_total) * 100)

#def check_null(x):
 # if pd.isnull(x).any():
  #  return False
  #return True

#df = df[df["choices"].apply(check_null)]

def label_choice(choice):
    if choice == 1:
        return "In-Favor"
    elif choice == 2:
        return "Against"

df['choice'] = df['choice'].apply(label_choice)

# Display the table
st.table(df)


