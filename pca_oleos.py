import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import altair as alt
    import matplotlib.pyplot as plt

    return mo, pd, plt


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


@app.cell
def _(df, mo):
    def norm(df,col='std'):
        df[col] = df[col] - df[col].mean()

    media_df = df.agg(['min', 'max', 'mean', 'std'], axis=1)
    norm(media_df)
    #media_df['std'] = media_df['std'] * (media_df.max().max()/media_df['std'].max())
    mo.ui.matplotlib(media_df.drop(columns=['std']).plot(figsize=(16,6)))
    return (media_df,)


@app.cell
def _(media_df, mo):
    mo.ui.matplotlib(media_df['std'].plot(figsize=(16,6),color='r'))
    return


@app.cell
def _(df, mo, plt):
    range = (1620,1685)
    fig = df[(df.index > min(range)) & (df.index < max(range))].T.boxplot(figsize=(16,7),grid=False)
    fig.tick_params(axis='x', labelrotation=90)
    mo.ui.matplotlib(plt.gca())
    return


if __name__ == "__main__":
    app.run()
