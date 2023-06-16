import requests
import json
import plotly.express as px

class Record:
    def __init__(self, series_id, period_year, value, footnotes):
        self.series_id = series_id
        self.period_year = period_year
        self.value = value
        self.footnotes = footnotes

# Function to decode period values to month names
def decode_period(period):
    month_map = {
        'M01': 'January',
        'M02': 'February',
        'M03': 'March',
        'M04': 'April',
        'M05': 'May',
        'M06': 'June',
        'M07': 'July',
        'M08': 'August',
        'M09': 'September',
        'M10': 'October',
        'M11': 'November',
        'M12': 'December'
    }
    return month_map.get(period, period)

headers = {'Content-type': 'application/json'}
data = json.dumps({"seriesid": ['CUUR0000SA0', 'SUUR0000SA0'], "startyear": "2020", "endyear": "2023"})
p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
json_data = json.loads(p.text)

records = []

for series in json_data['Results']['series']:
    series_id = series['seriesID']
    
    for item in reversed(series['data']):
        period = item['period']
        year = item['year']
        value = item['value']
        footnotes = ""
        
        for footnote in item['footnotes']:
            if footnote:
                footnotes = footnotes + footnote['text'] + ','
        
        if 'M01' <= period <= 'M12':
            period_year = decode_period(period) + ' ' + year
            record = Record(series_id, period_year, value, footnotes)
            records.append(record)

# Create a dataframe from the records
data = {
    'Series ID': [record.series_id for record in records],
    'Period_Year': [record.period_year for record in records],
    'Value': [float(record.value) for record in records],
    'Footnotes': [record.footnotes for record in records]
}
df = pd.DataFrame(data)

# Plotting connected scatter plot (x=Period_Year, y=Value)
fig = px.scatter(df, x='Period_Year', y='Value', color='Series ID', title='CPI for All Urban Consumers')
fig.update_traces(mode='lines+markers')

# Display the graph
fig.show()
