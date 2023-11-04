import pandas as pd
import streamlit as st
import plotly.express as px

# Set the page width m
st.set_page_config(page_title='Swiss Inflation Explorer (Beta)',page_icon= "🇨🇭",initial_sidebar_state="auto")

# Plot styling
line_shape = 'spline'


expander = st.sidebar.expander("Custom Colors")
with expander:
    col1, col2, col3, col4, col5 = st.columns(5)
    color1 = col1.color_picker('Main', '#037F8C')
    color2 = col2.color_picker('2nd', '#7ED0D9')
    color3 = col3.color_picker('3rd', '#01A5BD')
    color4 = col4.color_picker('4th', '#F27244')
    color5 = col5.color_picker('5th', '#F28F79')
    color6 = col1.color_picker('6th', '#368c7a')
    color7 = col2.color_picker('7th', '#7CB342')
    color8 = col3.color_picker('8th', '#0C8040')
    color9 = col4.color_picker('9th', '#1ad3aa')
    color10 = col5.color_picker('10th', '#F2B710')
    color11 = col1.color_picker('11th', '#a6b481')
    color12 = col2.color_picker('12th', '#15634d')
    color13 = col3.color_picker('13th', '#00aa85')
    color14 = col4.color_picker('14th', '#007754')
    color15 = col5.color_picker('15th', '#abd4c8')
    color16 = col1.color_picker('16th', '#d4c997')
    color17 = col2.color_picker('17th', '#bebf7a')
    color18 = col3.color_picker('18th', '#e2c48e')
    color19 = col4.color_picker('19th', '#9db784')
    color20 = col5.color_picker('20th', '#82a793')


    custom_color_sequence = [
        color1, color2, color3, color4, color5, color6, color7, color8, color9, color10,
        color11, color12, color13, color14, color15, color16, color17, color18, color19, color20
    ]


# import Data
df_weights = pd.read_csv('data/df_weights.csv')
df_inflation = pd.read_csv('data/df_inflation.csv')

# Page 1
def page1(df):
    st.title("Page 1")
    st.write("This is the content for Page 1.")
    #  Dropdown to select the year
    selected_year = st.selectbox("Select a Year", df.columns[2:])

    # Filter data for the selected year
    year_data = df[['Position', selected_year]]

    # Sort the DataFrame by the selected year in descending order
    year_data = year_data.sort_values(by=selected_year, ascending=False)

     # Donut Chart
    fig_donut = px.pie(
        year_data,
        names='Position',
        values=selected_year,
        hole=0.5,
        color_discrete_sequence=custom_color_sequence
    )

    fig_donut.update_traces(textposition='inside', textinfo='percent')
    fig_donut.update_layout(
        legend_title='Kategorie'
    )

    # Display the pie chart in the Streamlit app
    st.plotly_chart(fig_donut)

# Page 2
def page2():
    st.title("Page 2")
    st.write("This is the content for Page 2.")
    # Add more content for Page 2

# Create a navigation menu
page = st.sidebar.selectbox("Select a Page", ["Page 1", "Page 2"])

# Display the selected page
if page == "Page 1":
    page1(df_weights)
elif page == "Page 2":
    page2()

