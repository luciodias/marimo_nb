import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler, Normalizer

    return PCA, StandardScaler, mo, np, pd, plt


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
    f_range = (1620,1685)
    fig = df[(df.index > min(f_range)) & (df.index < max(f_range))].T.boxplot(figsize=(16,7),grid=False)
    fig.tick_params(axis='x', labelrotation=90)
    mo.ui.matplotlib(plt.gca())
    return


@app.cell
def _(PCA, StandardScaler, df, mo, np, pd):
    samples,n_vars = df.shape

    X = df.to_numpy()
    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA() #n_components=n_vars,)
    scores = pca.fit_transform(X_scaled)
    scores_df = pd.DataFrame(data=scores,columns=df.columns)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    loadings_df = pd.DataFrame(data=loadings, columns=[f'PC{(x+1)}' for x in range(n_vars)])
    mo.vstack([
        scores_df,
        loadings_df, 
    ]) 

    return loadings_df, scores_df


@app.cell
def _(loadings_df, mo, plt):
    _fig = plt.figure(figsize=(8, 6))
    _ax = _fig.add_subplot(111, projection='3d')
    scatter = _ax.scatter3D(loadings_df['PC1'], loadings_df['PC2'], loadings_df['PC3'],)
    _ax.set_xlabel('PC1')
    _ax.set_ylabel('PC2')
    _ax.set_zlabel('PC3')
    mo.ui.matplotlib(_fig.gca())
    return


@app.cell
def _(mo, plt, scores_df):
    _fig = plt.figure(figsize=(8, 6))
    _ax = _fig.add_subplot(111, projection='3d')
    _scatter = _ax.scatter3D(scores_df['azeite_oliva1'], scores_df['oleo_canola1'], scores_df['oleo_girassol1'],)
    _ax.set_xlabel('X')
    _ax.set_ylabel('Y')
    _ax.set_zlabel('Z')
    mo.ui.matplotlib(_fig.gca())
    return


@app.cell
def _(scores_df):
    scores_df.columns
    return


if __name__ == "__main__":
    app.run()
