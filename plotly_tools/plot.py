from plotly.subplots import make_subplots
import plotly.graph_objects as go


def __trace_or_list(trace_or_list):
    if isinstance(trace_or_list, list):
        return trace_or_list
    elif trace_or_list is not None:
        return [trace_or_list]


def __add_trace_to_fig(fig, row, col, trace, secondary_y):
    fig.add_trace(trace, row=row, col=col, secondary_y=secondary_y)
    fig.update_yaxes(
        title_text=trace.name,
        row=row,
        col=col,
        secondary_y=secondary_y
    )

    return fig


def build_trace(X, y, name, fill=None, mode="lines", text=None, extra_args={}):
    return go.Scatter(
        x=X,
        y=y,
        name=name,
        fill=fill,
        mode=mode,
        text=text,
        **extra_args
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


def plot_scatter(
    trace_list,
    title=None,
    identity=False,
    x_name=None,
    y_name=None,
    height=800
):
    fig = go.Figure()
    trace_list = __trace_or_list(trace_list)

    max_xy = -1e10
    min_xy = 1e10
    for trace in trace_list:
        max_xy = max(max(trace.x), max(trace.y), max_xy)
        min_xy = min(min(trace.x), min(trace.y), min_xy)
        fig.add_trace(trace)

    min_xy = min(min_xy, 0.0)
    points = [min_xy, max_xy]
    if identity:
        trace_id = build_trace(
            points,
            points,
            "Identity",
            extra_args={
                "line": {
                    "color": "black",
                    "dash": "dash"
                }
            })

        fig.add_trace(trace_id)
    fig.update_xaxes(title=x_name)
    fig.update_yaxes(title=y_name)

    fig.update_layout(
        height=height,
        width=height,
        title=go.layout.Title(
            text=title,
            xref="paper",
            x=0
        )
    )

    return fig


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


def bland_altman(data, col1, col2, name=None, text=None, title=None):
    mean = data[[col1, col2]].mean(axis=1)
    diff = data[col1] - data[col2]
    mean_diff = diff.mean()
    std_diff = diff.std()

    trace_ba = build_trace(
        mean,
        diff,
        name,
        mode="markers",
        text=text
    )

    max_val = mean_diff + 1.96 * std_diff
    points_x = [mean.min(), mean.max()]
    max_points_y = [max_val, max_val]
    min_val = mean_diff - 1.96*std_diff
    min_points_y = [min_val, min_val]
    trace_max = build_trace(
        points_x,
        max_points_y,
        f"+SD1.96: {max_val:.3f}",
        extra_args={"line": {"color": "black", "dash": "dash"}}
    )

    trace_min = build_trace(
        points_x,
        min_points_y,
        f"-SD1.96: {min_val:.3f}",
        extra_args={"line": {"color": "black", "dash": "dash"}}
    )

    return plot_scatter([
        trace_ba,
        trace_max,
        trace_min
    ], x_name="Mean", y_name="Diff", title=title)
