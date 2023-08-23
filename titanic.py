import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid, GridOptionsBuilder, ColumnsAutoSizeMode
import base64
import plotly.express as px
from dotenv import load_dotenv
import os
import requests

# FILES
from my_package.style import css_style,css_style_center,div_style_start,div_style_end
from my_package.html import title,html_code


# Set page configuration
st.set_page_config(layout="wide")

# Map secret
secret_dataappname = st.secrets["DataAppName"]

# Read the CSV file

file_path = "/data/in/tables/TitanicDemoData.csv"
df_data = pd.read_csv(file_path)


# Set logo image path and put in on to the right top
logo_image = os.path.abspath("/home/appuser/app/static/keboola.png")
logo_html = f'<div style="display: flex; justify-content: flex-end;"><img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 100px; margin-left: -10px;"></div>'
st.markdown(f"{logo_html}", unsafe_allow_html=True)

# Display the title and logo
#st.title("Titanic Demo Data App in Keboola")
st.title(secret_dataappname)

# Display the statistics subheader
st.markdown(title["statistics"],unsafe_allow_html=True)

# Assign the filtered data to a new DataFrame
df_filtered = df_data


st.markdown(css_style, unsafe_allow_html=True)

# Define metrics and corresponding icons
metrics = [
    ("Total People", "{:,}".format(np.count_nonzero(df_data['Sex'])).replace(",", " ")),
    ("Total Women", np.count_nonzero(df_data['Sex'] == 'female')),
    ("Total Men", np.count_nonzero(df_data['Sex'] == 'male')),
    ("Average Age", round(np.mean(df_data["Age"]), 1)),
    ("Women Average Age", round(df_data[df_data['Sex'] == 'female']['Age'].mean(), 1)),
    ("Men Average Age", round(df_data[df_data['Sex'] == 'male']['Age'].mean(), 1)),
    ("Total Survived People", np.count_nonzero(df_data['Survived'] == 1)),
    ("Total Survived Women", ((df_data['Sex'] == 'female') & (df_data['Survived'] == 1)).sum()),
    ("Total Survived Men", ((df_data['Sex'] == 'male') & (df_data['Survived'] == 1)).sum())
]


my_dict = {
    "Women Average Age": "age_group.png",
    "Women": "woman.png",
    "Age": "age_group.png",

    "People": "people.png",
    "Men": "man.png"
}

col1, col2, col3 = st.columns(3)

# Iterate over the metrics
for i, metric in enumerate(metrics):
    column_index = i % 3
    metric_label, metric_value = metric
    
    # Get the appropriate column based on the column index
    if column_index == 0:
        col = col1
    elif column_index == 1:
        col = col2
    else:
        col = col3
    
    # Find the corresponding icon for the metric label
    icon_path = None
    for key in my_dict.keys():
        if key in metric_label:
            icon_path = my_dict[key]
            break

# <img src="data:image/png;base64,{base64.b64encode(open(f"/data/in/files/{value}", 'rb').read()).decode()}" alt="Image" width="56" />

    if icon_path is not None:
        with col:
            icon_image = os.path.abspath(f"/home/appuser/app/static/{icon_path}")
            # Display the icon and metric information
            st.markdown(f'''
                <div class="div-container" style="display:flex; margin:10px">
                    <div class="div-icon" style="flex-basis:2">
                        <img src="data:image/png;base64,{base64.b64encode(open(icon_image, 'rb').read()).decode()}" alt="Image" width="56" />
                    </div>
                    <div style="flex-shrink:1; margin-left: 8%">
                        <h2 class="header">{metric_label}</h2>
                        <p class="text">{metric_value}</p>
                    </div>
                </div>
            ''', unsafe_allow_html=True)

# Display the "Filters" subheader
st.markdown(title["filters"], unsafe_allow_html=True)

col4, col8 = st.columns(2)

# Column 4
with col4:
    st.write(div_style_start, unsafe_allow_html=True)
    
    # List of unique sex in the dataframe
    sex = df_data["Sex"].unique().tolist()
    
    # Multiselect filter for gender
    sex_selection = st.multiselect("Gender", sex)
    
    # Filter the dataframe based on sex selection
    if sex_selection:
        df_filtered = df_filtered[df_data["Sex"].isin(sex_selection)]
    
    st.write(div_style_end, unsafe_allow_html=True)

# Column 8
with col8:
    st.write(div_style_start, unsafe_allow_html=True)
    
    # Define the options for the multi-select dropdown
    options = ["Unspecified", "Yes", "No"]
    
    # Multi-select dropdown for survived filter
    selected_options = st.multiselect("Survived", options)
    
    # Filter the data based on the selected options
    if "Yes" in selected_options:
        df_filtered = df_filtered[df_filtered["Survived"] == 1]
    if "No" in selected_options:
        df_filtered = df_filtered[df_filtered["Survived"] == 0]
    
    st.write(div_style_end, unsafe_allow_html=True)

# Age Filter
min_age_data = df_data["Age"].min().item()
max_age_data = df_data["Age"].max().item()

# Double-ended slider for age filter
age_slider_range = st.slider("Age", min_value=min_age_data, value=[min_age_data, max_age_data])

min_age = age_slider_range[0]
max_age = age_slider_range[1]

# Filter the data based on age range
df_filtered = df_filtered[(df_filtered["Age"] >= min_age) & (df_filtered["Age"] <= max_age)]

st.write('</div>', unsafe_allow_html=True)

# Display the "Titanic Analysis" subheader
st.markdown(title["titanic"], unsafe_allow_html=True)

# Display tabs for "Visualizations" and "Raw data"
tab1, tab2 = st.tabs(["Visualizations", "Raw data"])
st.container()


with tab1:
    st.markdown(title["dataTable"], unsafe_allow_html=True)
    
    # Select desired columns for the table
    selected_column = df_filtered[["Name", "Sex", "Survived", "Age", "Fare", "Boarded", "Destination"]]
    
    # Create a new DataFrame for the table
    df_for_table = pd.DataFrame(selected_column)
    
    # Configure grid options for the table
    gb = GridOptionsBuilder.from_dataframe(df_for_table)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=10)  # Add pagination
    gridOptions = gb.build()
    
    # Define column definitions for the table
    gridOptions['columnDefs'] = [
        {
            'headerName': 'Name',
            'field': 'Name',
            'flex': 1,
        },
        {
            'headerName': 'Gender',
            'field': 'Sex',
            'flex': 1,
        },
        {
            'headerName': 'Age',
            'field': 'Age',
            'sort': 'asc',
            'flex': 1,
        },
        {
            'headerName': 'Survived',
            'field': 'Survived',
            'sort': 'asc',
            'flex': 1,
        },
        {
            'headerName': 'Fare',
            'field': 'Fare',
            'flex': 1,
        },
        {
            'headerName': 'Boarded',
            'field': 'Boarded',
            'flex': 1,
        },
        {
            'headerName': 'Destination',
            'field': 'Destination',
            'flex': 1,
        },
        # Add more column definitions if needed
    ]
    
    # Display the AgGrid table
    AgGrid(df_for_table,
            gridOptions=gridOptions,
            theme='alpine',
            enable_enterprise_modules=False,
            columns_auto_size_mode=ColumnsAutoSizeMode.FIT_CONTENTS)
    
    chart1, chart2 = st.columns(2)
    
    # Prepare data for charts
    age_categories = pd.cut(df_filtered["Age"], bins=np.arange(0, 100, 10), right=False)
    age_counts = age_categories.value_counts().sort_index()
    survived_counts = df_filtered.groupby(age_categories)["Survived"].sum()
 
    with chart1:
        # Display the bar chart
        st.markdown('<p class="subheader-2">Survivors within Age Categories</p>', unsafe_allow_html=True)
        # Convert IntervalIndex to string representations
        age_categories_labels = [str(interval) for interval in age_counts.index]

        # Create a DataFrame for the data
        data = pd.DataFrame({
            'Age Category': age_categories_labels,
            'Total People': age_counts.values,
            'Survived': survived_counts.values
        })


        colors = ['#3CA0FF', '#2724ed']

        fig = px.bar(data, x='Age Category', y=['Total People', 'Survived'],
             labels={'x': 'Age Category', 'y': 'Number of People'},
             color_discrete_sequence=colors,
             barmode='group')


        fig.update_xaxes(title_text='Age Category')  # Set x-axis label
        fig.update_yaxes(title_text='Number of People')  # Set y-axis label
        # Display the Plotly figure
        st.plotly_chart(fig, use_container_width=True)
    


    with chart2:
        st.markdown('<p class="subheader-2">Probability of Survival by Age</p>', unsafe_allow_html=True)
        # Calculate the probability of survival by age categories
        age_probabilities = survived_counts / age_counts
        age_categories_labels = [f"{interval.left}-{interval.right}" for interval in age_probabilities.index]

        # Create a DataFrame for the probabilities and age categories
        prob_df = pd.DataFrame({'Age Category': age_categories_labels, 'Probability': age_probabilities})
        # Create a bar chart using Plotly Express
        fig = px.bar(prob_df, x='Age Category', y='Probability',
                    labels={'Probability': 'Probability'},
                    color_discrete_sequence=['#3CA0FF'])
        
        # Display the Plotly figure
        st.plotly_chart(fig, use_container_width=True)

    
with tab2:
    # Display raw data table
    st.markdown(title["rawData"], unsafe_allow_html=True)
    
    # Copy filtered data to a new DataFrame
    df_filtered_raw = df_filtered
    
    # Configure grid options for the raw data table
    raw = GridOptionsBuilder.from_dataframe(df_filtered_raw)
    raw.configure_pagination(paginationAutoPageSize=False, paginationPageSize=50)   # Add pagination
    
    st.dataframe(df_filtered)


# Add description section
st.markdown(title["description"], unsafe_allow_html=True)
      
st.write(html_code, unsafe_allow_html=True)
    
# Center the image using CSS styling
st.markdown(css_style_center,unsafe_allow_html=True)
    
# Display the logo with width and position centered to the right and to the left
st.markdown(
    f"""
    <div style="display: flex; justify-content: flex-end;">
        <div>
            <p><strong>Version:</strong> 1.1</p>
        </div>
        <div style="margin-left: auto;">
            <img src="data:image/png;base64,{base64.b64encode(open(logo_image, "rb").read()).decode()}" style="width: 100px;">
        </div>
    </div>
    """,
    unsafe_allow_html=True
)