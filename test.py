import streamlit as st
import pandas as pd
import json
import datetime
import altair as alt


def main():
    with open('codeforces_crawler//codeforces_crawler//spiders//codeforces_data.json') as f:
        data = json.load(f)
    user_handles = [item['handle'] for item in data]

    st.selectbox("this is label", user_handles,
                 on_change=modify_options(user_handles))


def modify_options():
    return


if __name__ == '__main__':
    main()
