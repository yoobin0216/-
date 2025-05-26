import pandas as pd

url = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"
df = pd.read_csv(url)
df.head()

import plotly.express as px

fig = px.line(df, x='날짜', y='값', title='날짜별 값 변화')
fig.show()
