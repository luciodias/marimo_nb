import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full")

with app.setup:
    #setup cell
    pass


@app.cell
def _():
    import marimo as mo
    import math
    import svg

    return math, mo, svg


@app.cell
def _(mo):
    n1 = mo.ui.slider(
        1.0, 2.5, 0.05, value=1.5, label="$n_1$ (meio 1)"
    )
    n2 = mo.ui.slider(
        1.0, 2.5, 0.05, value=1.0, label="$n_2$ (meio 2)"
    )
    theta1 = mo.ui.slider(
        0, 90, 1, value=45, label="$\\theta_1$ (°)"
    )
    return n1, n2, theta1


@app.cell
def _(math, n1, n2, theta1):
    t1 = math.radians(theta1.value)
    sn = n1.value * math.sin(t1) / n2.value
    total_internal = sn > 1.0
    t2 = math.asin(sn) if not total_internal else None
    theta2_deg = math.degrees(t2) if t2 is not None else None
    theta_c_deg = (
        math.degrees(math.asin(n2.value / n1.value))
        if n1.value > n2.value
        else None
    )
    return t1, t2, theta2_deg, theta_c_deg, total_internal


@app.cell
def _(math, mo, svg, t1, t2, total_internal):
    _L = 1.0
    _W, _H = 640.0, 540.0
    _XMIN, _XMAX = -1.6, 1.6
    _YMIN, _YMAX = -1.35, 1.35


    def _px(x, y):
        return (
            (x - _XMIN) / (_XMAX - _XMIN) * _W,
            (_YMAX - y) / (_YMAX - _YMIN) * _H,
        )


    def _ray(x1, y1, x2, y2, color):
        p1 = _px(x1, y1)
        p2 = _px(x2, y2)
        return svg.Line(
            x1=p1[0], y1=p1[1], x2=p2[0], y2=p2[1],
            stroke=color, stroke_width=3.5, stroke_linecap="round",
        )


    _px0 = _px(0.0, 0.0)[0]
    _py0 = _px(0.0, 0.0)[1]

    _elements = [
        svg.Line(x1=0.0, y1=_py0, x2=_W, y2=_py0, stroke="#94a3b8", stroke_width=2.5),
        svg.Line(x1=_px0, y1=0.0, x2=_px0, y2=_H, stroke="#94a3b8", stroke_width=1.5, stroke_dasharray=[5, 4]),
        _ray(0.0, 0.0, -_L * math.sin(t1), _L * math.cos(t1), "#f59e0b"),
        _ray(0.0, 0.0, _L * math.sin(t1), _L * math.cos(t1), "#3b82f6"),
    ]
    if not total_internal:
        _elements.append(
            _ray(0.0, 0.0, -_L * math.sin(t2), -_L * math.cos(t2), "#10b981")
        )

    for _label, _dy in [("n\u2081", 0.9), ("n\u2082", -0.9)]:
        _p = _px(0.75, _dy)
        _elements.append(
            svg.Text(x=_p[0], y=_p[1], text=_label, font_size=24, font_style="italic", fill="#475569")
        )

    _tp = _px(0.0, 1.24)
    _elements.append(
        svg.Text(x=_tp[0], y=_tp[1], text="Lei de Snell \u2014 Descartes", font_size=17,
                 font_weight="bold", text_anchor="middle", fill="#1e293b")
    )

    _legend_y = 46
    _legend = [
        (180, "#f59e0b", "Incidente"),
        (280, "#3b82f6", "Refletida"),
        (382, "#10b981", "Refratada"),
    ]
    for _lx, _lcolor, _llabel in _legend:
        _elements.append(
            svg.Line(x1=_lx, y1=_legend_y, x2=_lx + 26, y2=_legend_y,
                     stroke=_lcolor, stroke_width=3.5, stroke_linecap="round")
        )
        _elements.append(
            svg.Text(x=_lx + 32, y=_legend_y + 4, text=_llabel, font_size=13, fill="#334155")
        )

    chart = mo.Html(
        svg.SVG(
            width=640,
            height=540,
            viewBox=svg.ViewBoxSpec(0, 0, 640, 540),
            elements=_elements,
        ).as_str()
    )
    return (chart,)


@app.cell
def _(theta2_deg, theta_c_deg, total_internal):
    if total_internal:
        status = "Reflexão total interna"
        status_color = "#dc2626"
    else:
        status = "Refração"
        status_color = "#059669"

    theta2 = f"{theta2_deg:.1f}°" if theta2_deg is not None else "—"
    info = f"**θ₂** = {theta2}"
    if theta_c_deg is not None:
        info += f" &nbsp;|&nbsp; **θ_c** = {theta_c_deg:.1f}°"
    info += (
        f" &nbsp;|&nbsp; **Status:** "
        f"<span style='color:{status_color}'>{status}</span>"
    )
    return


@app.cell
def _(n1):
    n1
    return


@app.cell
def _(n2):
    n2
    return


@app.cell
def _(theta1):
    theta1
    return


@app.cell
def _(chart):
    chart
    return


if __name__ == "__main__":
    app.run()
