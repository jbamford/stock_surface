import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd


def plotdf(df):
    data = [
        go.Surface(
            z=df.as_matrix(),
        )
    ]
    layout = go.Layout(
        title='Mt Bruno Elevation',
        autosize=False,
        scene=dict(

            yaxis=dict(
                nticks=50, range=[0, 1000],),

        ),
        width=900,
        height=500,
        xaxis=dict(
            nticks=20,
            range=[0, 10]
        ),
        yaxis=dict(
            range=[0, 1000]
        ),
        margin=dict(
            l=10,
            r=10,
            b=10,
            t=10
        )
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='elevations-3d-surface')
