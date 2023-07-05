import altair as alt
import datetime
import streamlit as st
import json
import requests
import pandas as pd
import pycountry as pc


def update_dropdown_menu():
    return


def main():

    data = []
    handle_tuples = []
    handles = []
    default_index = 0
    with open('codeforces_crawler\\codeforces_crawler\\spiders\\cf_user_data.jl') as file:
        for i, line in enumerate(file):
            json_obj = json.loads(line)
            data.append(json_obj)
            handle_tuples.append((json_obj['handle'], i))
            if json_obj['handle'] in 'y0urs3lf':
                default_index = i
    handles = [t[0] for t in handle_tuples]

    st.write("# Codeforces User's Profile")

    # the index argument is to parse the default value to the selectbox
    handle = st.selectbox("Select a handle", handles,
                          index=default_index, on_change=update_dropdown_menu())
    index = handle_tuples[handles.index(handle)][1]

    # Extract and display the response
    if True:
        user_info = data[index]
        rank = user_info['rank'][0:len(user_info['rank'])-1]
        color = get_color(rank)
        cur_handle = user_info["handle"]

        # current rank and handle
        st.markdown(
            f'<h3 style="color:{color}; padding-bottom: 0px">{rank.title()}</h3> <h2 style="color:{color}; padding-top: 0px">{cur_handle}</h2>', unsafe_allow_html=True)

        # flag image and country
        country = "Viet Nam" if user_info["country"] == "Vietnam" else user_info["country"]
        if country != "":
            country_code = get_country_code(country).lower()
            image_url = f'https://codeforces.org/s/33207/images/flags-16/{country_code}.png'
            st.markdown(
                f'<p><img src="{image_url}"> <strong>{country}</strong> </p>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<p><strong>{country}</strong> </p>',
                unsafe_allow_html=True
            )

        # rating
        st.markdown(
            f'<p><strong>Rating:</strong> <strong style="color:{color}">{str(user_info["rating"])}</strong></p>',
            unsafe_allow_html=True
        )

        # max rating
        max_rating_color = get_color(user_info["max_rank"])
        st.markdown(
            f'<p> <strong>Max Rating: </strong><strong style="color:{max_rating_color}">{str(user_info["max_rating"])}, </strong> <strong style="color:{max_rating_color}">{user_info["max_rank"].title()}</strong>', unsafe_allow_html=True
        )
    else:
        pass

    # request data to render the chart
    # return
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
