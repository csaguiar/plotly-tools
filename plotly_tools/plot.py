from plotly.subplots import make_subplots
import plotly.graph_objects as go


def __trace_or_list(trace_or_list):
    if isinstance(trace_or_list, list):
        return trace_or_list
    elif trace_or_list is not None:
        return [trace_or_list]


def __add_trace_to_fig(fig, row, col, trace, secondary_y):
    fig.add_trace(trace, row=row, col=col)
    fig.update_yaxes(
        title_text=trace.name,
        row=row,
        col=col,
        secondary_y=secondary_y
    )

    return fig


def build_trace(X, y, name, fill=None):
    return go.Scatter(
        x=X,
        y=y,
        name=name,
        fill=fill
    )


def build_traces_from_dataframe(df, fill={}):
    return [
        build_trace(serie.index, serie, name, fill=fill.get(name))
        for name, serie in df.items()
    ]


def list_traces_to_input(traces_list, mode="alone", trace_secondary=None):
    if mode == "alone":
        return [(trace, None) for trace in traces_list]
    if mode == "repeat_sec":
        return [(trace, trace_secondary) for trace in traces_list]


def plot_traces(trace_list, title=None, extra_args={}, height_factor=200):
    total_num_plots = len(trace_list)

    fig = make_subplots(
        rows=total_num_plots,
        cols=1,
        shared_xaxes=True,
        specs=[[{'secondary_y': True}] for _ in range(total_num_plots)],
        **extra_args
    )

    for i, (trace_primary, trace_secondary) in enumerate(trace_list):
        trace_primary = __trace_or_list(trace_primary)
        trace_secondary = __trace_or_list(trace_secondary)

        for trace in trace_primary:
            fig = __add_trace_to_fig(fig, i+1, 1, trace, False)

        if trace_secondary is not None:
            for trace in trace_secondary:
                fig = __add_trace_to_fig(fig, i+1, 1, trace, True)

    fig.update_xaxes(title="time", row=total_num_plots, col=1)
    fig.update_layout(
        height=height_factor*(total_num_plots),
        title=go.layout.Title(
            text=title,
            xref="paper",
            x=0
        )
    )

    return fig
