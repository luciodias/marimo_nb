import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt

    return mo, pd


@app.cell
def _(pd):
    df = pd.read_csv('raman/spectra_oleos_comestiveis.csv', 
                     index_col='R.Shift',sep=',', encoding='utf-8')
    #df = df.drop(columns=['azeite_oliva', 'oleo_canola media',])
    filtro = [_x for _x in df.columns if 'media' in _x]
    filtro.append('azeite_oliva')
    df = df.drop(columns=filtro)
    return (df,)


@app.cell
def _(df, mo):
    mo.ui.matplotlib(df.plot(figsize=(16,6),
                             title='Espectros',
                             grid=True,
                             xlabel=r'$cm^-1$',
                            ))
    return


if __name__ == "__main__":
    app.run()
