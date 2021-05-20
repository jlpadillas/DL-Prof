import plotly.express as px
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


def get_rates_from_df_pivot(df):

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

def get_rates_from_df(df):

    # Setting the dict of rate and the events needed to perform the operation
    events_dict = {
        "IPC": ["instructions", "cycles"],
        "Branch acc.": ["branch-misses", "branch-instructions"],
        "L1 rate": ["L1-dcache-load-misses", "L1-dcache-loads"]
    }

    events = df["Event Name"].unique()
    cpus = df["CPU"].unique()
    num_events = len(events)
    num_cpus = len(cpus)
    num_measures = int(len(df.index) / (num_events * num_cpus))

    # for i in cpus:
    #     dff = df[df['CPU'] == i]
    #     for j in range(1, num_measures + 1):
    #         dfff = dff[dff["# Measure"] == j]
    #         for k, v in events_dict.items():
    #             if ((dfff['Event Name'] == v[0]) & (df['Event Name'] == v[1])).any():

    #                 pass
            # if dfff[dfff["Event Name"] == "cycles"]

    for k, v in events_dict.items():
        # The events have been measured
        if v[0] in events and v[1] in events:
            v_0 = df[df["Event Name"] == v[0]]
            v_1 = df[df["Event Name"] == v[1]]
            dff = v_0.div(v_1)
            # df[k] = dff
            df = df.append(dff, ignore_index=True)
            # print(v_0, v_1)
        # if (v_0 & v_1).any():
            # print(v_0, v_1)
        # if v[0] in df.columns and v[1] in df.columns:
            # aux = calculate_rate(df[v[0]].tolist(), df[v[1]].tolist())
            # df[k] = aux
    print(df)
    return df
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


import plotly.graph_objects as go

import pandas as pd

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

name_html = "strides.html"
fig.write_html(name_html)

exit(0)
# e
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
# Creates the array with the # of measure
num_measure = 1
df.insert(0, "# Measure", num_measure)
# We have to modify them depending on the number of measures and cpus
for i in range(int(len(df.index) / len_per_measure), 0, -1):
    df.loc[df.index[-i * len_per_measure:], "# Measure"] = num_measure
    num_measure += 1


# # "Rotate" the table
# df = df.pivot_table(index=["# Measure", "CPU"], columns=[
#     "Event Name"], values=["Value"]).fillna(0)
# # Drop the first multiindex
# df.columns = df.columns.droplevel()
# # Add columns with rates (IPC, acc., etc.)
# df = get_rates_from_df_pivot(df)
# # Remove name of columns
# # df.columns.name = None
# # Reset the index to an auto-increment
# # df = df.reset_index()

# # stack the changes
# # srs = df.stack()
# # # Add name to the colum

# # header = srs.columns()
# # header[-1] = "Value"
# # df.rename(header)
# # print(df)
# # exit(0)


# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #


import plotly.graph_objects as go
import pandas as pd


# df = get_rates_from_df(df)

# # Group params to pass them to plotly
# df_T = df.transpose()
# hd = list(df.columns)
# # hd.insert(0, "CPU")
# bd = list(df.values)
# # bd.insert(0, df.index)

# fig = go.Figure(data=[go.Table(
#     header=dict(values=hd, fill_color='paleturquoise', align='left'),
#     cells=dict(values=bd, fill_color='lavender', align='left'))
# ])

# # Display it at the end of execution
# fig.show()
# # Save it in a file and don't open it now
# # fig.write_html(html_file)


# dff = px.data.gapminder()
# print(df)
# print(dff)

# fig = px.bar(df, x="Event Name", y="Value", color="Event Name",
#              animation_frame="# Measure", animation_group="# Measure", range_y=[0, 600_000_000])

fig = px.scatter(df, x="Event Name", y="Value", animation_frame="# Measure", animation_group="# Measure",
                 size="Value", color="Event Name", hover_name="Event Name",facet_col="Event Name",
                 log_x=False, size_max=55, range_x=[-1, 4], range_y=[0, 1_000_000_000])
# fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
#            size="pop", color="continent", hover_name="country", facet_col="continent",
#            log_x=True, size_max=45, range_x=[100,100000], range_y=[25,90])




fig.show()


# print(df)

exit(0)
# ----------------------------------------------------------------------- #
# ----------------------------------------------------------------------- #

df = px.data.gapminder()
# fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
#            size="pop", color="continent", hover_name="country",
#            log_x=True, size_max=55, range_x=[100,100000], range_y=[25,90])

# fig.show()


print(df.index)


exit(0)


df = px.data.gapminder()
print(df)
fig = px.scatter(df, x="gdpPercap", y="lifeExp", animation_frame="year", animation_group="country",
                 size="pop", color="continent", hover_name="country",
                 log_x=True, size_max=55, range_x=[100, 100000], range_y=[25, 90])

fig.show()


exit(0)


# url = "https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv"
# dataset = pd.read_csv(url)

# years = ["1952", "1962", "1967", "1972", "1977", "1982", "1987", "1992", "1997", "2002",
#          "2007"]

measures = list(range(1, num_measure + 1))

# make list of continents
# continents = []
# for continent in dataset["continent"]:
#     if continent not in continents:
#         continents.append(continent)
# make figure
fig_dict = {
    "data": [],
    "layout": {},
    "frames": []
}

# fill in most of layout
# fig_dict["layout"]["xaxis"] = {"range": [30, 85], "title": "Life Expectancy"}
fig_dict["layout"]["xaxis"] = {
    "range": [0, num_measure * 3], "title": "# measure"}
# fig_dict["layout"]["yaxis"] = {"title": "GDP per Capita", "type": "log"}
fig_dict["layout"]["yaxis"] = {"title": "Value", "type": "log"}
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
        "prefix": "# measure:",
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

# # make data
# year = 1952
# for continent in continents:
#     dataset_by_year = dataset[dataset["year"] == year]
#     dataset_by_year_and_cont = dataset_by_year[
#         dataset_by_year["continent"] == continent]
#     # print(dataset_by_year_and_cont)

#     data_dict = {
#         "x": list(dataset_by_year_and_cont["lifeExp"]),
#         "y": list(dataset_by_year_and_cont["gdpPercap"]),
#         "mode": "markers",
#         "text": list(dataset_by_year_and_cont["country"]),
#         "marker": {
#             "sizemode": "area",
#             "sizeref": 200000,
#             "size": list(dataset_by_year_and_cont["pop"])
#         },
#         "name": continent
#     }
#     fig_dict["data"].append(data_dict)
#     print(data_dict)

# make data
pos_measure = measures[0]
cpu = available_cpus[0]
idx = pd.IndexSlice
for event in events_measured:
    # dataset_by_position = df.loc[idx[pos_measure, :]]
    dataset_by_position_and_cpu = df.loc[idx[pos_measure, cpu]]

    data_dict = {
        "x": list(dataset_by_position_and_cpu),
        # "y": list(dataset_by_position_and_cpu["gdpPercap"]),
        "mode": "markers",
        # "text": list(dataset_by_position_and_cpu["Event Name"]),
        "marker": {
            "sizemode": "area",
            # "sizeref": 200000,
            "size": list(dataset_by_position_and_cpu)
        },
        "name": event
    }
    fig_dict["data"].append(data_dict)
    # print(dataset_by_position_and_cpu["Event Name"])
    print(data_dict)

exit(0)
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
