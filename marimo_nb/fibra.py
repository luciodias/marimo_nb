import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full")

with app.setup:
    #setup cell
    pass


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import altair as alt
    import math

    return alt, math


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
def _(alt, math, t1, t2, total_internal):
    L = 1.0
    incident = [
        {"x": -L * math.sin(t1), "y": L * math.cos(t1), "ray": "Incidente"},
        {"x": 0.0, "y": 0.0, "ray": "Incidente"},
    ]
    reflected = [
        {"x": 0.0, "y": 0.0, "ray": "Refletida"},
        {"x": L * math.sin(t1), "y": L * math.cos(t1), "ray": "Refletida"},
    ]
    segments = incident + reflected
    if not total_internal:
        segments += [
            {"x": 0.0, "y": 0.0, "ray": "Refratada"},
            {
                "x": -L * math.sin(t2),
                "y": -L * math.cos(t2),
                "ray": "Refratada",
            },
        ]

    rays = (
        alt.Chart(segments)
        .mark_line(strokeWidth=3.5, strokeCap="round")
        .encode(
            x=alt.X(
                "x:Q",
                scale=alt.Scale(domain=[-1.6, 1.6]),
                axis=alt.Axis(title=None),
            ),
            y=alt.Y(
                "y:Q",
                scale=alt.Scale(domain=[-1.3, 1.3]),
                axis=alt.Axis(title=None),
            ),
            color=alt.Color(
                "ray:N",
                legend=alt.Legend(title="Raio", orient="top"),
                scale=alt.Scale(
                    domain=["Incidente", "Refletida", "Refratada"],
                    range=["#f59e0b", "#3b82f6", "#10b981"],
                ),
            ),
        )
        .properties(width=640, height=520, title="Lei de Snell — Descartes")
    )

    interface = (
        alt.Chart([{"y": 0.0}])
        .mark_rule(stroke="#94a3b8", strokeWidth=2.5)
        .encode(y="y:Q")
    )
    normal = (
        alt.Chart([{"x": 0.0}])
        .mark_rule(stroke="#94a3b8", strokeWidth=1.5, strokeDash=[5, 4])
        .encode(x="x:Q")
    )
    labels = (
        alt.Chart(
            [
                {"x": 0.75, "y": 0.9, "text": "n₁"},
                {"x": 0.75, "y": -0.9, "text": "n₂"},
            ]
        )
        .mark_text(fontSize=24, fontStyle="italic", color="#475569")
        .encode(x="x:Q", y="y:Q", text="text:N")
    )

    chart = alt.layer(interface, normal, rays, labels)
    return


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


if __name__ == "__main__":
    app.run()
