import altair as alt
import datetime
import streamlit as st
import json
import requests
import pandas as pd
import pycountry as pc


data = []
user_handles = []


titles = []
time_limits = []
memory_limits = []
input_files = []
output_files = []
problem_statements = []
input_specifications = []
output_specifications = []
sample_test_input = []
sample_test_output = []
note = []


def main():
    read_user_info()
    read_problemset()
    user_info_tab, problemset_tab = st.tabs(
        ["📈 User Info", "🗃 Problemset"])

    show_user_info_ui(user_info_tab)
    show_problemset_ui(problemset_tab)


def show_user_info_ui(tab):
    tab.write("# Codeforces User's Profile")

    # the index argument is to parse the default value to the selectbox
    default_index = user_handles.index("y0urs3lf")
    handle = tab.selectbox(
        "Select a handle", user_handles, index=default_index)

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
        tab.markdown(
            f'<h3 style="color:{color}; padding-bottom: 0px">{rank.title()}</h3> <h2 style="color:{color}; padding-top: 0px">{cur_handle}</h2>', unsafe_allow_html=True)

        # flag image and country
        country = "Viet Nam" if user_info["country"] == "Vietnam" else user_info["country"]
        country_code = get_country_code(country).lower()
        image_url = f'https://codeforces.org/s/33207/images/flags-16/{country_code}.png'
        tab.markdown(
            f'<p><img src="{image_url}"> <strong>{country}</strong> </p>',
            unsafe_allow_html=True
        )

        # rating
        tab.markdown(
            f'<p><strong>Rating:</strong> <strong style="color:{color}">{str(user_info["rating"])}</strong></p>',
            unsafe_allow_html=True
        )

        # max rating
        maxRating_color = get_color(user_info["maxRank"])
        tab.markdown(
            f'<p> <strong>Max Rating: </strong><strong style="color:{maxRating_color}">{str(user_info["maxRating"])}, </strong> <strong style="color:{maxRating_color}">{user_info["maxRank"].title()}</strong>', unsafe_allow_html=True
        )
    else:
        # write the error
        tab.write(f'**Error:**{response["comment"]}')

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
        tab.altair_chart(chart, use_container_width=True)
    else:
        tab.write(f'**Error:**{response["comment"]}')


def read_user_info():
    # get handles from JSON file
    with open('codeforces_crawler\codeforces_crawler\spiders\cf_user_handle_vn.json') as f:
        data = json.load(f)
        for item in data:
            user_handles.append(item['handle'])


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


def show_problemset_ui(tab):
    tab.markdown('<h1>Codeforces Problemset</h1>', unsafe_allow_html=True)
    button_frames = []
    selected_problem_id = -1
    for i in range(len(titles)):
        button_frame = tab.empty()
        isClicked = button_frame.button(
            titles[i][0], use_container_width=True, key=i)
        button_frames.append((button_frame, i))
        if isClicked:
            selected_problem_id = i
            break
        # show_problem()

    if selected_problem_id != -1:
        for (frame, i) in button_frames:
            frame.empty()
        tab.write(
            """
                <script>
                window.scrollTo({ top: 0, behavior: 'smooth' });
                </script>
                """,
            unsafe_allow_html=True,
        )
        isClicked = tab.button("Back to Problemset")
        show_problem(i, tab)

        if isClicked:
            selected_problem_id = -1


def show_problem(i, tab):
    tab.markdown(f'<h1>{titles[i][0]}</h1>', unsafe_allow_html=True)
    tab.write(f'{time_limits[i][0]}": "{time_limits[i][1]}')
    tab.write(f'{memory_limits[i][0]}": "{memory_limits[i][1]}')
    tab.write(f'{input_files[i][0]}": "{input_files[i][1]}')
    tab.write(f'{output_files[i][0]}": "{output_files[i][1]}')

    tab.write("**Problem:**")
    for p in problem_statements[i]:
        new_p = "".join(p)
        tab.markdown(new_p)

    tab.write("**Input:**")
    for p in input_specifications[i]:
        new_p = "".join(p)
        tab.markdown(new_p)

    tab.write("**Output:**")
    for p in output_specifications[i]:
        new_p = "".join(p)
        tab.markdown(new_p)

    tab.write("**Examples**")
    for i, (inp, out) in enumerate(zip(sample_test_input[i], sample_test_output[i])):
        # print(p)
        test = ["**input**",
                inp, "**output**", out]
        df = pd.DataFrame({
            f'Test {i}': test
        })

        # tab.write(df.to_markdown(index=False), unsafe_allow_html=True)
        tab.write(f'**Test {i}**')
        tab.write('**input**')
        tab.text(inp)
        tab.write('**output**')
        tab.text(out)

    tab.divider()


def read_problemset():
    with open('codeforces_crawler\codeforces_crawler\spiders\problem_data.jl', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i > 50:
                break
            json_obj = json.loads(line)

            titles.append(json_obj["title"])
            time_limits.append(json_obj['time_limit'])
            memory_limits.append(json_obj['memory_limit'])
            input_files.append(json_obj['input_file'])
            output_files.append(json_obj['output_file'])
            problem_statements.append(json_obj['problem_statement'])
            input_specifications.append(json_obj['input_specification'])
            output_specifications.append(json_obj['output_specification'])
            sample_test_input.append(json_obj['sample_test_input'])
            sample_test_output.append(json_obj['sample_test_output'])
            note.append(json_obj['note'])


if __name__ == '__main__':
    main()
