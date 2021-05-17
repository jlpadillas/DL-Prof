import plotly.graph_objects as go

import pandas as pd


# ----------------------------------------------------------------------- #
def calculate_rate(dividend, divisor):
    aux = []
    if len(dividend) != len(divisor):
        return aux

    for i in range(0, len(dividend)):
        aux.append(dividend[i] / divisor[i])

    return aux
# ----------------------------------------------------------------------- #


def get_rates_from_df(df):

    # Setting the dict of rate and the events needed to perform the operation
    events_dict = {
        "IPC": ["instructions", "cycles"],
        "Branch acc.": ["branch-misses", "branch-instructions"],
        "L1 rate": ["L1-dcache-load-misses", "L1-dcache-loads"]
    }

    for k, v in events_dict.items():
        if v[0] in df.columns and v[1] in df.columns:
            aux = calculate_rate(df[v[0]].tolist(), df[v[1]].tolist())
            df[k] = aux

    return df
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #

csv_file = "out/mnist_each_epoch.csv"

# Read csv with the following header
header = ["CPU", "Value", "Unit", "Event Name"]
df = pd.read_csv(csv_file, header=None, sep=":", names=header)

# Get the list of CPUs measured
available_cpus = df["CPU"].unique()
# And the events
events_measured = df["Event Name"].unique()


# Calculate the # of measures in function of the #cpus and #events
len_per_measure = len(events_measured) * len(available_cpus)
measures = list(range(1, int(len(df.index) / len_per_measure) + 1))
# Add a new column with the value of the list
df.insert(0, "# Measure", measures)

print(df)
exit(0)

# Add to the first column the # of measure
num_measure = 0
df.insert(0, "# Measure", num_measure)
# We have to modify them depending on the number of measures and cpus
len_per_df = len(events_measured) * len(available_cpus)
for i in range(int(len(df.index) / len_per_df), 0, -1):
    df.loc[df.index[-i * len_per_df:], "# Measure"] = num_measure
    num_measure += 1



df = df.pivot_table(index=["# Measure", "CPU"], columns=[
    "Event Name"], values=["Value"]).fillna(0)
# Drop the first multiindex
df.columns = df.columns.droplevel()

df = get_rates_from_df(df)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #



url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
dataset = pd.read_csv(url)

years = ["1952", "1962", "1967", "1972", "1977", "1982", "1987", "1992", "1997", "2002",
         "2007"]

# make list of continents
continents = []
for continent in dataset["continent"]:
    if continent not in continents:
        continents.append(continent)
# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

# fill in most of layout
fig_dict["layout"]["xaxis"] = {"range": [30, 85], "title": "Life Expectancy"}
fig_dict["layout"]["yaxis"] = {"title": "GDP per Capita", "type": "log"}
fig_dict["layout"]["hovermode"] = "closest"
fig_dict["layout"]["updatemenus"] = [
    {
        "buttons": [
            {
                "args": [None, {"frame": {"duration": 500, "redraw": False},
                                "fromcurrent": True, "transition": {"duration": 300,
                                                                    "easing": "quadratic-in-out"}}],
                "label": "Play",
                "method": "animate"
            },
            {
                "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                  "mode": "immediate",
                                  "transition": {"duration": 0}}],
                "label": "Pause",
                "method": "animate"
            }
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 87},
        "showactive": False,
        "type": "buttons",
        "x": 0.1,
        "xanchor": "right",
        "y": 0,
        "yanchor": "top"
    }
]

sliders_dict = {
    "active": 0,
    "yanchor": "top",
    "xanchor": "left",
    "currentvalue": {
        "font": {"size": 20},
        "prefix": "Year:",
        "visible": True,
        "xanchor": "right"
    },
    "transition": {"duration": 300, "easing": "cubic-in-out"},
    "pad": {"b": 10, "t": 50},
    "len": 0.9,
    "x": 0.1,
    "y": 0,
    "steps": []
}

# make data
year = 1952
for continent in continents:
    dataset_by_year = dataset[dataset["year"] == year]
    dataset_by_year_and_cont = dataset_by_year[
        dataset_by_year["continent"] == continent]

    data_dict = {
        "x": list(dataset_by_year_and_cont["lifeExp"]),
        "y": list(dataset_by_year_and_cont["gdpPercap"]),
        "mode": "markers",
        "text": list(dataset_by_year_and_cont["country"]),
        "marker": {
            "sizemode": "area",
            "sizeref": 200000,
            "size": list(dataset_by_year_and_cont["pop"])
        },
        "name": continent
    }
    fig_dict["data"].append(data_dict)

# make frames
for year in years:
    frame = {"data": [], "name": str(year)}
    for continent in continents:
        dataset_by_year = dataset[dataset["year"] == int(year)]
        dataset_by_year_and_cont = dataset_by_year[
            dataset_by_year["continent"] == continent]

        data_dict = {
            "x": list(dataset_by_year_and_cont["lifeExp"]),
            "y": list(dataset_by_year_and_cont["gdpPercap"]),
            "mode": "markers",
            "text": list(dataset_by_year_and_cont["country"]),
            "marker": {
                "sizemode": "area",
                "sizeref": 200000,
                "size": list(dataset_by_year_and_cont["pop"])
            },
            "name": continent
        }
        frame["data"].append(data_dict)

    fig_dict["frames"].append(frame)
    slider_step = {"args": [
        [year],
        {"frame": {"duration": 300, "redraw": False},
         "mode": "immediate",
         "transition": {"duration": 300}}
    ],
        "label": year,
        "method": "animate"}
    sliders_dict["steps"].append(slider_step)


fig_dict["layout"]["sliders"] = [sliders_dict]

fig = go.Figure(fig_dict)

fig.show()
