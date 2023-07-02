import streamlit as st
import pandas as pd
import json
import datetime
import altair as alt

with open('test.json') as f:
    data = json.load(f)

contestName, rating, time, rank = [], [], [], []
for x in data:
    contestName.append(x.get("contestName"))
    rating.append(x.get("newRating"))

    timestamp = x.get("ratingUpdateTimeSeconds")
    dt_object = datetime.datetime.fromtimestamp(timestamp)
    formatted_date = dt_object.strftime('%Y-%m-%d')
    time.append(formatted_date)
    rank.append(x.get("rank"))

chart_data = pd.DataFrame(
    {
        'contestName': contestName,
        'rating': rating,
        'time': time,
        'rank': rank,
    })

y_min = max(0, min(chart_data["rating"]) - 100)
y_max = max(chart_data["rating"]) + 100

scale = alt.Scale(domain=(y_min, y_max))

chart = alt.Chart(chart_data).mark_line(point=alt.OverlayMarkDef(size=50, filled=True)).encode(
    x='time:T',
    y=alt.Y('rating', scale=scale),
    tooltip=['contestName', 'rank']).interactive()

# Render the chart using Streamlit
st.altair_chart(chart, use_container_width=True)
