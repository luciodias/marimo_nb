import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", layout_file="layouts/slide.slides.json")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Teste

    \[c \approx 2,997.10^8 m/s\]

    $$  \frac{1}{2} \sum_{k=1}^nn \leq  $$

    \[f(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \ldots.\]

    $$\begin{align}
    a &= 2 + 2 \\
    &= 4
    \end{align}$$

    # Cheat sheet

    ≤ $\leq ≥ \geq 6 = \neq ≈ \approx
    × \times ÷ \div ± \pm · \cdot
    ◦ ^{\circ} ◦ \circ ′ \prime · · · \cdots
    ∞ \infty ¬ \neg ∧ \wedge ∨ \vee
    ⊃ \supset ∀ \forall ∈ \in → \rightarrow
    ⊂ \subset ∃ \exists /∈ \notin ⇒ \Rightarrow
    ∪ \cup ∩ \cap | \mid ⇔ \Leftrightarrow
    ˙a \dot a ˆa \hat a ¯a \bar a ˜a \tilde a
    α \alpha β \beta γ \gamma δ \delta
     \epsilon ζ \zeta η \eta ε \varepsilon
    θ \theta ι \iota κ \kappa ϑ \vartheta
    λ \lambda μ \mu ν \nu ξ \xi
    π \pi ρ \rho σ \sigma τ \tau
    υ \upsilon φ \phi χ \chi ψ \psi
    ω \omega Γ \Gamma ∆ \Delta Θ \Theta
    Λ \Lambda Ξ \Xi Π \Pi Σ \Sigma
    Υ \Upsilon Φ \Phi Ψ \Psi Ω \Omega
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    https://the0cp.cc/posts/mathjax/

    $$\vec{a} \quad
    \bar{a}
    \top
    \bot \newline
    \angle$$

    asdas

    \[ x^n + y^n = z^n \]



    \begin{matrix}
    1&0&0\\
    0&1&0\\
    0&0&1\\
    \end{matrix}



    \begin{bmatrix}
    {a_{11}}&{a_{12}}&{\cdots}&{a_{1n}}\\
    {a_{21}}&{a_{22}}&{\cdots}&{a_{2n}}\\
    {\vdots}&{\vdots}&{\ddots}&{\vdots}\\
    {a_{m1}}&{a_{m2}}&{\cdots}&{a_{mn}}\\
    \end{bmatrix}



    \begin{cases}
    a_1x+b_1y+c_1z=d_1\\
    a_2x+b_2y+c_2z=d_2\\
    a_3x+b_3y+c_3z=d_3\\
    \end{cases}

    $$a_1x+b_1y+c_1z=d_1 \tag{1}$$
    """)
    return


if __name__ == "__main__":
    app.run()
