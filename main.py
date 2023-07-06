import altair as alt
import datetime
import streamlit as st
import json
import requests
import pandas as pd
import pycountry as pc


def main():
    # get handles from JSON file
    with open('codeforces_crawler\codeforces_crawler\spiders\cf_user_handle_vn.json') as f:
        data = json.load(f)
    user_handles = [item['handle'] for item in data]

    st.write("# Codeforces User's Profile")

    # the index argument is to parse the default value to the selectbox
    default_index = user_handles.index("y0urs3lf")
    handle = st.selectbox("Select a handle", user_handles, index=default_index)

    # request the response from codeforces
    url = f"https://codeforces.com/api/user.info?handles={handle}"
    response = requests.get(url).json()

    # Extract and display the response
    if response["status"] == "OK":
        user_info = response["result"][0]
        rank = user_info["rank"]
        color = get_color(rank)
        cur_handle = user_info["handle"]

        # current rank and handle
        st.markdown(
            f'<h3 style="color:{color}; padding-bottom: 0px">{rank.title()}</h3> <h2 style="color:{color}; padding-top: 0px">{cur_handle}</h2>', unsafe_allow_html=True)

        # flag image and country
        country = "Viet Nam" if user_info["country"] == "Vietnam" else user_info["country"]
        country_code = get_country_code(country).lower()
        image_url = f'https://codeforces.org/s/33207/images/flags-16/{country_code}.png'
        st.markdown(
            f'<p><img src="{image_url}"> <strong>{country}</strong> </p>',
            unsafe_allow_html=True
        )

        # rating
        st.markdown(
            f'<p><strong>Rating:</strong> <strong style="color:{color}">{str(user_info["rating"])}</strong></p>',
            unsafe_allow_html=True
        )

        # max rating
        maxRating_color = get_color(user_info["maxRank"])
        st.markdown(
            f'<p> <strong>Max Rating: </strong><strong style="color:{maxRating_color}">{str(user_info["maxRating"])}, </strong> <strong style="color:{maxRating_color}">{user_info["maxRank"].title()}</strong>', unsafe_allow_html=True
        )
    else:
        # write the error
        st.write("**Error:**", response["comment"])

    # request data to render the chart
    url = f"https://codeforces.com/api/user.rating?handle={handle}"
    response = requests.get(url).json()

    if response["status"] == "OK":
        data = response["result"]

        contestName, rating, time, rank = [], [], [], []
        for x in data:
            contestName.append(x.get("contestName"))
            rating.append(x.get("newRating"))

            # convert time from unix-format -> date
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

        # altair support rendering chart with limit value in the axis
        y_min = max(0, min(chart_data["rating"]) - 100)
        y_max = max(chart_data["rating"]) + 100

        scale = alt.Scale(domain=(y_min, y_max))

        chart = alt.Chart(chart_data).mark_line(
            point=alt.OverlayMarkDef(
                size=50, filled=False, color="#4A55A2", fill="#A0BFE0"),  # properties of the point
            color="#A0BFE0"  # color of the line
        ).encode(
            x='time:T',  # the :T is added to display x-axis as Time, not String => more interactive
            # the alt.y is added to show the points in certain range
            y=alt.Y('rating', scale=scale),
            tooltip=['contestName', 'rank'],
        ).interactive()

        # Render the chart using Streamlit
        st.altair_chart(chart, use_container_width=True)
    else:
        st.write("**Error:**", response["comment"])


def get_color(rank):
    if rank == "international grandmaster":
        return "red"
    if rank == "grandmasterr":
        return "red"
    if rank == "international master":
        return "orange"
    if rank == "master":
        return "orange"
    if rank == "candidate master":
        return "purple"
    if rank == "expert":
        return "blue"
    if rank == "specialist":
        return "cyan"
    if rank == "pupil":
        return "green"
    return "grey"


def get_country_code(country_name):
    try:
        country = pc.countries.get(name=country_name)
        return country.alpha_2
    except AttributeError:
        return None


if __name__ == '__main__':
    main()
