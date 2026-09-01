import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mtick
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler, Normalizer

    return PCA, StandardScaler, mo, mtick, pd, plt


@app.cell
def _(pd):
    df = pd.read_csv('raman/spectra_oleos_comestiveis.csv', 
                     index_col='R.Shift',sep=',', encoding='utf-8')
    #df = df.drop(columns=['azeite_oliva', 'oleo_canola media',])
    filtro = [_x for _x in df.columns if 'media' in _x]
    filtro.append('azeite_oliva')
    df = df.drop(columns=filtro)

    p_conf = {'figsize': (12, 4),}
    return df, p_conf


@app.cell
def _(df, mo, p_conf):
    mo.ui.matplotlib(df.plot(title='Espectros',
                             grid=True,
                             xlabel=r'$cm^-1$',
                             **p_conf,
                            ))
    return


@app.cell
def _(df, mo, p_conf):
    def norm(df,col='std'):
        df[col] = df[col] - df[col].mean()

    media_df = df.agg(['min', 'max', 'mean', 'std'], axis=1)
    norm(media_df)
    #media_df['std'] = media_df['std'] * (media_df.max().max()/media_df['std'].max())
    mo.ui.matplotlib(media_df.drop(columns=['std']).plot(**p_conf))
    return (media_df,)


@app.cell
def _(media_df, mo, p_conf):
    mo.ui.matplotlib(media_df['std'].plot(color='r',title='Desvio Padrão',**p_conf,))
    return


@app.cell
def _(df, mo, p_conf, plt):
    f_range = (1620,1685)
    fig = df[(df.index > min(f_range)) & (df.index < max(f_range))].T.boxplot(grid=False,**p_conf,)
    fig.tick_params(axis='x', labelrotation=90)
    mo.ui.matplotlib(plt.gca())
    return


@app.cell
def _(PCA, StandardScaler, df, mo, p_conf, pd):
    samples,n_vars = df.shape

    X = df.to_numpy()
    X_scaled = StandardScaler().fit_transform(X)
    pca = PCA() #n_components=n_vars,)
    scores = pca.fit_transform(X_scaled)
    scores_df = pd.DataFrame(data=scores,index=df.index)
    loadings = pca.components_.T # * np.sqrt(pca.explained_variance_)
    loadings_df = pd.DataFrame(data=loadings,index=df.columns) #columns=[f'PC{(x+1)}' for x in range(n_vars)])
    mo.vstack([
        mo.ui.matplotlib(scores_df[[0,1,2]].plot(title='Scores',**p_conf,)),
        mo.ui.matplotlib(loadings_df[[0,1,2]].plot(title='Loadings',**p_conf,)),
    ]) 
    return loadings_df, pca


@app.cell
def _(mo, mtick, p_conf, pca, pd):
    _var_data = pca.explained_variance_
    var_df = pd.Series(data=_var_data,index=range(1, len(_var_data) + 1))
    var_df = pd.concat([pd.Series([0], index=[0]), var_df], ignore_index=True)
    _var_sum = var_df.sum().sum()
    _ax = var_df.cumsum().plot(title='Variancia',**p_conf,)
    _ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals=1,xmax=_var_sum))
    _ax.set_ylim(bottom=0) 
    _ax.set_ylabel('Porcentagem (%)')
    mo.ui.matplotlib(_ax)
    return


@app.cell
def _(loadings_df, mo, p_conf, plt):
    _fig = plt.figure(**p_conf,)
    _ax = _fig.add_subplot(111, projection='3d')
    scatter = _ax.scatter3D(loadings_df[0], loadings_df[1], loadings_df[2],)
    _ax.set_xlabel('PC1')
    _ax.set_ylabel('PC2')
    _ax.set_zlabel('PC3')
    mo.ui.matplotlib(_fig.gca())
    return


@app.cell
def _():
    import subprocess
    result = subprocess.run(["git", "status","-s"], capture_output=True, text=True)
    print("Output:", result.stdout.strip().split("\n"))
    #print("Return Code:", result.returncode)

    return


@app.cell
def _(df):
    grupos = {
        "Azeite":"azeite",
        "Maria":"maria",
        "Canola":"canola",
        "Milho":"milho",
        "Girassol":"girassol",
        "Soja":"soja",
    }
    classe = {}

    for grupo in grupos:
        classe[grupo]=[x for x in df.columns if grupos[grupo] in x]

    print(classe)

    classe = {}

    for col in df.columns:
        for g in grupos:
            if grupos[g] in col and not classe.get(col):
                classe[col]=g
                break
    print(classe)
    return


if __name__ == "__main__":
    app.run()
