import altair as alt
import datetime
import streamlit as st
import json
import pandas as pd


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
    read_data()
    show_ui()


def show_ui():
    st.markdown('<h1>Codeforces Problemset</h1>', unsafe_allow_html=True)
    button_frames = []
    selected_problem_id = -1
    for i in range(len(titles)):
        button_frame = st.empty()
        isClicked = button_frame.button(
            titles[i][0], use_container_width=True, key=i)
        button_frames.append((button_frame, i))
        if isClicked:
            selected_problem_id = i
            break
        # show_problem()

    if selected_problem_id != -1:
        for (frame, i) in button_frames:
            if i != selected_problem_id:
                frame.empty()
        isClicked = st.button("Back to Problemset")
        show_problem(i)

        if isClicked:
            selected_problem_id = -1


def show_problem(i):
    st.markdown(f'<h1>{titles[i][0]}</h1>', unsafe_allow_html=True)
    st.write(time_limits[i][0], ":", time_limits[i][1])
    st.write(memory_limits[i][0], ":", memory_limits[i][1])
    st.write(input_files[i][0], ":", input_files[i][1])
    st.write(output_files[i][0], ":", output_files[i][1])

    st.write("**Problem:**")
    for p in problem_statements[i]:
        new_p = "".join(p)
        st.markdown(new_p)

    st.write("**Input:**")
    for p in input_specifications[i]:
        new_p = "".join(p)
        st.markdown(new_p)

    st.write("**Output:**")
    for p in output_specifications[i]:
        new_p = "".join(p)
        st.markdown(new_p)

    st.write("**Examples**")
    for i, (inp, out) in enumerate(zip(sample_test_input[i], sample_test_output[i])):
        # print(p)
        test = ["**input**",
                inp, "**output**", out]
        df = pd.DataFrame({
            f'Test {i}': test
        })

        # st.write(df.to_markdown(index=False), unsafe_allow_html=True)
        st.write(f'**Test {i}**')
        st.write('**input**')
        st.text(inp)
        st.write('**output**')
        st.text(out)

    st.divider()


def read_data():
    with open('codeforces_crawler\codeforces_crawler\spiders\problem_data.jl', encoding='utf-8') as file:
        for i, line in enumerate(file):
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
