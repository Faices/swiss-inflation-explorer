import pandas as pd
import streamlit as st
import plotly.express as px

# Set the page width m
st.set_page_config(page_title='Swiss Inflation Explorer (Beta)',page_icon= "🇨🇭",initial_sidebar_state="collapsed")

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




st.title("🇨🇭 Swiss Inflation Explorer")
st.write("Exploring Swiss Inflation: Analyzing Trends Since 1983 and Comparing the Effects of Changing Denomination Currency.")


#############################
#### Exchange Rates Load ####
#############################

def process_exchange_rate_data(file_path, sheet_name, exchange_rate_column, new_column_name):
    # Read the Excel file with the specified header row
    exchange_rate_df = pd.read_excel(file_path, sheet_name=sheet_name)

    # Select the relevant columns and sort by 'Year'
    exchange_rate_df = exchange_rate_df[['Year', exchange_rate_column]]
    exchange_rate_df = exchange_rate_df.sort_values(by='Year', ascending=True)

    # Calculate the percentage change in exchange rate and add it as a new column
    exchange_rate_df[new_column_name] = exchange_rate_df[exchange_rate_column].pct_change()

    return exchange_rate_df

# Replace 'your_file.xlsx' with the path to your Excel file
file_path = 'data/exchangerates.xlsx'

chf_euro = process_exchange_rate_data(file_path, 'CHF_EUR', 'Average CHF/EUR', 'Exchange Rate Change') # Process CHF/EUR data
chf_usd = process_exchange_rate_data(file_path, 'CHF_USD', 'Average CHF/USD', 'Exchange Rate Change') # Process CHF/USD data)
chf_xbt = process_exchange_rate_data(file_path, 'CHF_XBT', 'Average CHF/XBT', 'Exchange Rate Change') # Process CHF/Bitcoin data)
chf_xau = process_exchange_rate_data(file_path, 'CHF_XAU', 'Average CHF/XAU', 'Exchange Rate Change') # Process CHF/Gold data)
chf_gbp = process_exchange_rate_data(file_path, 'CHF_GBP', 'Average CHF/GBP', 'Exchange Rate Change') # Process CHF/GBP data)
chf_try = process_exchange_rate_data(file_path, 'CHF_TRY', 'Average CHF/TRY', 'Exchange Rate Change') # Process CHF/TRY data)
chf_xag = process_exchange_rate_data(file_path, 'CHF_XAG', 'Average CHF/XAG', 'Exchange Rate Change') # Process CHF/TRY data)
chf_chf = process_exchange_rate_data(file_path, 'CHF_CHF', 'Average CHF/CHF', 'Exchange Rate Change') # Process CHF/CHF data) #Kontrolle Logik


#############################
#### Selections ####
#############################


# List of options
exchange_rate_options = ['CHF','EUR', 'USD', 'GBP','TRY','GOLD','SILVER','BTC']

# Create a selectbox
st.divider()

selected_currency_option = st.selectbox('Choose Currency Denomination', exchange_rate_options)

# Store the selected option in a variable
if selected_currency_option == 'EUR':
    exchange_rate_df = chf_euro
elif selected_currency_option == 'USD':
    exchange_rate_df = chf_usd
elif selected_currency_option == 'BTC':
    exchange_rate_df = chf_xbt
elif selected_currency_option == 'GOLD':
    exchange_rate_df = chf_xau
elif selected_currency_option == 'GBP':
    exchange_rate_df = chf_gbp
elif selected_currency_option == 'CHF':
    exchange_rate_df = chf_chf
elif selected_currency_option == 'TRY':
    exchange_rate_df = chf_try
elif selected_currency_option == 'SILVER':
    exchange_rate_df = chf_xag

# Define the range of years
years = [int(year) for year in exchange_rate_df['Year']]
start_year = min(years)
end_year = max(years)

# Create a dropdown widget to select the year
selected_year = st.selectbox("Choose a Base Year", years)

# Store the selected option in a variable
if selected_currency_option == 'EUR':
    exchange_rate_df = chf_euro
elif selected_currency_option == 'USD':
    exchange_rate_df = chf_usd
elif selected_currency_option == 'BTC':
    exchange_rate_df = chf_xbt
elif selected_currency_option == 'GOLD':
    exchange_rate_df = chf_xau
elif selected_currency_option == 'GBP':
    exchange_rate_df = chf_gbp
elif selected_currency_option == 'CHF':
    exchange_rate_df = chf_chf



#############################
#### Calculate Inflatiom ####
#############################

def read_inflation_data(file_path, sheet_name, last_valid_entry, level):
    # Read the Excel file with the specified header row
    data = pd.read_excel(file_path, sheet_name=sheet_name, header=3)
    df = data.iloc[:last_valid_entry + 1]  # This will keep rows up to the last_valid_entry
    df = df[df["Level"] == level]  # Select Level in inflation data (default 2)

    return df

def apply_exchange_rate_conversion(df, selected_year, end_year, exchange_rate_df):
    # Select the columns you want to adjust in df
    start_year = selected_year + 1

    # Generate a list of integers from start_year to end_year
    cols_to_adjust = list(range(start_year, end_year + 1))

    # Exchange Rate Conversion Logic
    if exchange_rate_df is not None:
        # Create a dictionary from exchange rate DataFrame
        exchange_rate_change_dict = exchange_rate_df.set_index('Year')['Exchange Rate Change'].to_dict()

        # Adjust the values in df based on the exchange rate change
        for col in cols_to_adjust:
            year = int(col)
            df[col] = df[col] + (exchange_rate_change_dict.get(year, 0) * 100)

    return df

def calculate_cumulative_inflation(df, selected_year):
    # Cumulative Inflation Logic
    # Set the dynamic year values to 100
    df.loc[:, selected_year] = 100

    # Loop through years and calculate real values and subtract 100, starting from the dynamic year
    for year in range(selected_year + 1, 2023):
        df[year] = df[year - 1] * (1 + df[year] / 100)

    for year in range(selected_year, 2023):
        df[year] = df[year] - 100

    subset_columns = ['PosTxt_E', 'PosNo', selected_year] + list(range(selected_year + 1, 2023))
    df = df[subset_columns]
    df = df.rename(columns={'PosNo': 'ID'})

    return df


# Example usage with chf_euro DataFrame
file_path = 'data/su-e-05.02.67.xlsx'
sheet_name = 'VAR_y-1'
last_valid_entry = 415


# Process inflation data with the specified exchange rate DataFrame
df_inflation_l2 = read_inflation_data(file_path, sheet_name, last_valid_entry,level=2)
df_inflation_exchange_adjusted_l2 = apply_exchange_rate_conversion(df_inflation_l2, selected_year, end_year, exchange_rate_df)
df_inflation_cumulative_l2 = calculate_cumulative_inflation(df_inflation_exchange_adjusted_l2, selected_year)

df_inflation_l1 = read_inflation_data(file_path, sheet_name, last_valid_entry,level=1)
df_inflation_exchange_adjusted_l1 = apply_exchange_rate_conversion(df_inflation_l1, selected_year, end_year, exchange_rate_df)
df_inflation_cumulative_l1 = calculate_cumulative_inflation(df_inflation_exchange_adjusted_l1, selected_year)


# Reshape the data into long format
df_inflation_cumulative_l2_long = pd.melt(df_inflation_cumulative_l2 , id_vars=['ID', 'PosTxt_E'], var_name='Year', value_name='Value')
df_inflation_cumulative_l1_long = pd.melt(df_inflation_cumulative_l1, id_vars=['ID', 'PosTxt_E'], var_name='Year', value_name='Value')

# Line chart using Plotly in the first column
fig_line = px.line(df_inflation_cumulative_l1_long,
                x='Year',
                y='Value',  # Pass both indicators as a list
                title="",
                line_shape=line_shape,
                color_discrete_sequence=custom_color_sequence)  # Add colors for each indicator

fig_line.update_layout(
    xaxis_title='',  # Hide the title of the x-axis
    yaxis_title='Cumulative rate of inflation in %',
    legend_title_text=''  # Hide the title of the x-axis
)

st.plotly_chart(fig_line,
                use_container_width=True,
                auto_open=False)

st.caption(f"Abbildung 1: Swiss Inflation from {start_year} - {end_year} denominated in {selected_currency_option}")


# Line chart using Plotly in the first column
fig_line = px.line(df_inflation_cumulative_l2_long,
                x='Year',
                y='Value',  # Pass both indicators as a list
                color='PosTxt_E',
                title="",
                line_shape=line_shape,
                color_discrete_sequence=custom_color_sequence)  # Add colors for each indicator

fig_line.update_layout(
    xaxis_title='',  # Hide the title of the x-axis
    yaxis_title='Cumulative rate of inflation in %',
    legend_title_text=''  # Hide the title of the x-axis
)

st.plotly_chart(fig_line,
                use_container_width=True,
                auto_open=False)

st.caption(f"Abbildung 2: Swiss Inflation by Categories from {start_year} - {end_year} denominated in {selected_currency_option}")


### Dataframe with line ####
df_development = df_inflation_cumulative_l2
df_development ["Development"] = df_development .apply(lambda row: row[2:].tolist(), axis=1)
df_development = df_development [["PosTxt_E","Development",2022]]
df_development.reset_index(drop=True, inplace=True)

st.dataframe(
    df_development,
    column_config={
        "PosTxt_E": "Category",
        "Development": st.column_config.LineChartColumn(
            "Cumulative rate of inflation in %",
            width="medium",
            help="Cumulative rate of inflation in %"),
        "2022":"Total rate of inflation in %"
    },
    hide_index=True,
    use_container_width = True
)

#########################
##### Basekt Weights ####
#########################

valid_gp_values = [1,2,3,4,5,6,7,8,9,10,11,12]
def process_excel_data(file_path,
                    sheet_name,
                    header_row,
                    last_valid_entry,
                    valid_column,
                    year_columns,
                    id_column,
                    id_column_name,
                    additional_columns=None):
    
    data = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
    data = data.iloc[:last_valid_entry + 1]

    filtered_data = data[data[valid_column].isin(valid_gp_values)]
    selected_columns = additional_columns + [valid_column] + year_columns
    filtered_data = filtered_data[selected_columns]
    filtered_data = filtered_data.rename(columns={valid_column: id_column_name})

    return filtered_data

file_path = 'data/su-d-05.02.90.xlsx'

# Process 2020 data
df_b_l2_20 = process_excel_data(file_path, 'LIK2020', 3, 415, 'PosNo', [2021, '2022', '2023'], 'PosNo', 'ID', additional_columns=['PosTxt_E'])

# Process 2015 data
valid_PosNo_15 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
df_b_l2_15 = process_excel_data(file_path, 'LIK2015', 3, 396, 'PosNo', [2016, 2017, '2018', '2019', '2020'], 'PosNo', 'ID', additional_columns=['PosTxt_E'])

# Process 2010 data
valid_gp_values_10 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
df_b_l2_10 = process_excel_data(file_path, 'LIK2010', 3, 313, 'GP Nr.', [2011, 2012, 2013, 2014, 2015], 'GP Nr.', 'ID', additional_columns=['deutsch'])

# Process 2005 data
valid_gp_values_05 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
df_b_l2_05 = process_excel_data(file_path, 'LIK2005', 3, 313, 'GP Nr.', [2006, 2007, 2008, 2009, 2010], 'GP Nr.', 'ID', additional_columns=['deutsch'])

# Process 2000 data
valid_gp_values_00 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
df_b_l2_00 = process_excel_data(file_path, 'LIK2000', 3, 313, 'Nr. ', ['2000/01', 2002, 2003, 2004, 2005], 'Nr. ', 'ID', additional_columns=['Position'])

# Start with df_b_l2_00 and perform left joins in the reverse order
left_merged_df = pd.merge(df_b_l2_00, df_b_l2_05, on='ID', how='left')
left_merged_df = pd.merge(left_merged_df, df_b_l2_10, on='ID', how='left')
left_merged_df = pd.merge(left_merged_df, df_b_l2_15, on='ID', how='left')
left_merged_df = pd.merge(left_merged_df, df_b_l2_20, on='ID', how='left')
left_merged_df.columns = left_merged_df.columns.astype(str)
df_weights = left_merged_df[['Position','ID','2000/01','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021','2022','2023']]
df_weights = df_weights.rename(columns={'2000/01': '2001'})
columns_to_convert = df_weights .columns[2:]  # Assuming the percentage columns start from the 3rd column
df_weights[columns_to_convert] = df_weights [columns_to_convert] / 100 # convert to decimal


selected_year = st.selectbox("Select a Year", df_weights.columns[2:])

# Filter data for the selected year
year_data = df_weights[['Position', selected_year]]

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
    



