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

    return PCA, StandardScaler, mo, pd, plt


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
    mo.ui.matplotlib(media_df['std'].plot(figsize=(16,6),color='r',title='Desvio Padrão'))
    return


@app.cell
def _(df, mo, plt):
    f_range = (1620,1685)
    fig = df[(df.index > min(f_range)) & (df.index < max(f_range))].T.boxplot(figsize=(16,7),grid=False)
    fig.tick_params(axis='x', labelrotation=90)
    mo.ui.matplotlib(plt.gca())
    return


@app.cell
def _(PCA, StandardScaler, df, mo, pd):
    samples,n_vars = df.shape

    X = df.to_numpy()
    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA() #n_components=n_vars,)
    scores = pca.fit_transform(X_scaled)
    scores_df = pd.DataFrame(data=scores,) #columns=df.columns)
    loadings = pca.components_.T # * np.sqrt(pca.explained_variance_)
    loadings_df = pd.DataFrame(data=loadings,) #columns=[f'PC{(x+1)}' for x in range(n_vars)])
    mo.vstack([
        mo.ui.matplotlib(scores_df[[0,1,2]].plot(figsize=(16, 4),title='Scores')),
        mo.ui.matplotlib(loadings_df[[0,1,2]].plot(figsize=(16, 4),title='Loadings')),
    ]) 
    return (loadings_df,)


@app.cell
def _(loadings_df, mo, plt):
    _fig = plt.figure(figsize=(8, 6))
    _ax = _fig.add_subplot(111, projection='3d')
    scatter = _ax.scatter3D(loadings_df[0], loadings_df[1], loadings_df[2],)
    _ax.set_xlabel('PC1')
    _ax.set_ylabel('PC2')
    _ax.set_zlabel('PC3')
    mo.ui.matplotlib(_fig.gca())
    return


if __name__ == "__main__":
    app.run()
