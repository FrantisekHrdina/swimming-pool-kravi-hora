#!/usr/bin/env python3

import plotly.graph_objs as go
import pandas as pd
import datetime
import sys
from datetime import date

df = pd.read_csv('/home/franta_hrdina/scripts/pool_stats/pool_stats.txt')

week_start = datetime.date(2019, 7, 22)
interval = datetime.timedelta(days=7)

while week_start <= datetime.datetime.now().date():
    week_data = df.loc[(df['timestamp'] > str(week_start)) & (df['timestamp'] < str(week_start + interval))]

    occupancy_in = go.Bar(
        x=week_data['timestamp'],
        y=week_data['occupancy_in'],
        name='Occupancy in',
        text=week_data['occupancy_in'],
        textposition='auto'
    )
    layout_in = go.Layout(
        title='Obsazenost krytého vnitřního bazénu {0} - {1}/ Occupancy of inner swimming pool'.format(week_start, week_start + interval),
        xaxis=go.layout.XAxis(
            tickformat="%a %d.%m.<br>%H:%M",
            showgrid=True

        ),
        yaxis=dict(
            title='počet návštěvníků / sum of visitors',
        )
    )
    fig_in = go.Figure(data=occupancy_in, layout=layout_in)
    fig_in.update_xaxes(ticks="inside")
    fig_in.write_html('/var/www/my_web/pool_stats/graphs/occupancy_in/occupancy_in_' + str(week_start) + '.html', auto_open=True)

    occupancy_out = go.Bar(
        x=week_data['timestamp'],
        y=week_data['occupancy_out'],
        name='Occupancy out',
        text=week_data['occupancy_out'],
        textposition='auto'
    )

    layout_out = go.Layout(
        title='Obsazenost venkovních bazénů {0} - {1}/ Occupancy of outer swimming pools'.format(week_start, week_start + interval),
        xaxis=go.layout.XAxis(
            tickformat="%a %d.%m.<br>%H:%M",
            showgrid=True
        ),
        yaxis=dict(
            title='počet návštěvníků / sum of visitors',
            titlefont_size=16,
            tickfont_size=14,
        ),
    )

    fig_out = go.Figure(data=occupancy_out, layout=layout_out)
    fig_out.update_xaxes(ticks="inside")
    fig_out.write_html('/var/www/my_web/pool_stats/graphs/occupancy_out/occupancy_out_' + str(week_start) + '.html', auto_open=True)

    air_temp_out = go.Bar(
        x=week_data['timestamp'],
        y=week_data['air_temp_out'],
        name='Air temperature out',
        text=week_data['air_temp_out'],
        textposition='auto'
    )

    layout_temp_out = go.Layout(
        title='Teplota sportovní areál Kraví hora {0} - {1}/ Air temperature at Kraví hora'.format(week_start, week_start + interval),
        xaxis=go.layout.XAxis(
            tickformat="%a %d.%m.<br>%H:%M",
            showgrid=True

        ),
        yaxis=dict(
            title='teplota vzduchu / air tempearature',
        )
    )

    fig_temp = go.Figure(data=air_temp_out, layout=layout_temp_out)
    fig_temp.update_xaxes(ticks="inside")
    fig_temp.write_html('/var/www/my_web/pool_stats/graphs/air_temp_out/air_temp_out_' + str(week_start) + '.html', auto_open=True)

    week_start = week_start + interval

today = date.today()
today_data = df.loc[(df['timestamp'] > str(today))]

occupancy_today = go.Bar(
    x=today_data['timestamp'],
    y=today_data['occupancy_in'],
    name='Occupancy in',
    text=today_data['occupancy_in'],
    textposition='auto'
)
layout_today = go.Layout(
    title='Obsazenost krytého vnitřního bazénu {0} / Occupancy of inner swimming pool'.format(today),
    xaxis=go.layout.XAxis(
        tickformat="%a %d.%m.<br>%H:%M",
        showgrid=True

    ),
    yaxis=dict(
        title='počet návštěvníků / sum of visitors',
    )
)
fig_in = go.Figure(data=occupancy_today, layout=layout_today)
fig_in.update_xaxes(ticks="inside")
fig_in.write_html('/var/www/my_web/pool_stats/graphs/occupancy_in/occupancy_today.html', auto_open=True)

