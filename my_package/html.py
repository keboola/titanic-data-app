

title= {
    "statistics":'<p class="subheader">Statistics</p>',
    "filters":'<p class="subheader">Filters</p>',
    "titanic":'<p class="subheader">Titanic Analysis</p>',
    "dataTable":'<p class="subheader-2">Data Table</p>',
    "survivors":'<p class="subheader-2">Survivors within Age Categories</p>',
    "probability":'<p class="subheader-2">Probability of Survival by Age Categories</p>',
    "rawData":'<p class="subheader-2">Raw Data</p>',
    "description":'<p class="subheader">Description</p>',
}

# Create two centered columns with filters and metrics information
html_code = '''
    <div style="display: flex; justify-content: center;">
        <div style="width: 50%;text-align:left">
            <strong>Filters:</strong>
            <p></p>
            <p>Gender: Passenger's gender (male, female).</p>
            <p>Age: Passengers' age on the Titanic.</p>
            <p>Survived: Indicates passenger survival status.</p>
        </div>
        <div style="width: 50%;text-align:left">
            <strong>Metrics:</strong>
            <p></p>
            <p>Total: The total number of people or categorized by gender.</p>
            <p>Average Age: The average age of all passengers or categorized by gender.</p>
            <p>Total Survived: The total number of survivors among all passengers or categorized by gender.</p>
        </div>
    </div>
    '''