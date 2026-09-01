import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import copy
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler, Normalizer

    return mo, np


@app.cell
def _(mo, np):
    def to_latex(arr,m_type='b',_dec=3):
        if m_type not in ['p','b','B','v','V']:
            m_type = ''
        if isinstance(arr,np.matrix):
            arr = np.asarray(arr)
        if arr.ndim == 1:
            arr = arr[np.newaxis, :]
        lines = [f"\\begin{{{m_type}matrix}}"]
        for row in arr:
            lines.append("  " + " & ".join([f'{x:.{_dec}f}' for x in row]) + " \\\\")
        lines.append(f"\\end{{{m_type}matrix}}")
        return mo.md(f"$$\n{"\n".join(lines)}\n$$")

    return (to_latex,)


@app.cell
def _(mo):
    _value = [
        [2.5,0.5,2.2,1.9,3.1,2.3,2.0,1.0,1.5,1.1],
        [2.4,0.7,2.9,2.2,3.0,2.7,1.6,1.1,1.6,0.9],
    ]
    dados = mo.ui.matrix(
        label = 'Dados',
        row_labels = ['x1','x2'],
        debounce = False,
        precision = 2,
        step = 0.05,
        value = _value,
    )
    return (dados,)


@app.cell
def _(dados, mo, np):
    data_matrix = np.matrix(dados.value)
    data_mean = data_matrix.mean(axis=1)
    mo.vstack([
        dados,
        mo.md(f'Média para $x1$ = {data_mean.A1[0]:.2f} <br> Média para $x2$ = {data_mean.A1[1]:.2f}'),
    ])
    return data_matrix, data_mean


@app.cell
def _(data_matrix, data_mean, mo):
    d_norm = data_matrix - data_mean
    _data_std = mo.ui.matrix(
        label = 'Dados Padronizados',
        row_labels = ['x1','x2'],
        debounce = True,
        precision = 2,
        step=1e-10,
        value = d_norm,
    )
    _data_std
    return (d_norm,)


@app.cell
def _(d_norm, mo, np, to_latex):
    _cov = np.cov(d_norm)
    _c = mo.ui.matrix(
        _cov,
        label = 'Dados Padronizados',
        precision = 4,
        step=1e-10,    
    )
    mo.hstack([
        mo.md('C ='),
        to_latex(_cov),
    ],align='center', justify='start')
    return


if __name__ == "__main__":
    app.run()
