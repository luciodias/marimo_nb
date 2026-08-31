import marimo

__generated_with = "0.24.0"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler, Normalizer

    return Normalizer, PCA, mo, np, pd, plt


@app.cell
def _(Normalizer, PCA, np, pd):
    data = pd.DataFrame.from_dict({
    "Variable A":[1,3,4,5,6,7,8,10,11,12,13],
    "Variable B":[1,3,6,4,7,9,12,13,8,13,14],
    "Variable C":[3,8,12,7,11,2,1,6,9,7,4],
    "Variable D":[14,7,5,5,1,9,12,8,3,10,11],
    "Variable E":[13,9,14,11,8,6,7,4,2,5,3],
    })
    samples,vars = data.shape

    X = data.to_numpy()
    # 2. Standardize the data (Crucial step for PCA)
    X_scaled = Normalizer().fit_transform(X)

    pca = PCA(n_components=vars,)
    scores = pca.fit_transform(X_scaled)
    scores_df = pd.DataFrame(data=scores, columns=data.columns)
    loadings = pca.components_.T * np.sqrt(pca.explained_variance_)
    loadings_df = pd.DataFrame(data=loadings, columns=[f'PC{(x+1)}' for x in range(vars)],)

    print(vars,samples)
    print(scores_df)
    print(loadings_df)
    return loadings_df, pca, scores


@app.cell
def _(loadings_df, mo, plt, scores):

    pc_list = loadings_df.columns

    plt.figure(figsize=(6, 6))
    plt.scatter(scores[:, 0], scores[:, 1], alpha=0.6)
    # Plota cada vetor (loading)
    for _feature in loadings_df.index:
        # Vetores vermelhos partindo da origem (0,0)
        plt.arrow(0, 0, loadings_df.loc[_feature, 'PC1'], loadings_df.loc[_feature, 'PC2'], 
                  color='crimson', head_width=0.04, head_length=0.04, linewidth=2, length_includes_head=True)
        # Texto identificando a variável original
        plt.text(loadings_df.loc[_feature, 'PC1'] * 1.1, loadings_df.loc[_feature, 'PC2'] * 1.1, 
                  _feature+1, color='crimson', ha='center', va='center', fontsize=11, fontweight='bold')

    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.title('PCA Biplot (Scores and Loadings)')
    plt.grid(True)
    scores_g = mo.ui.matplotlib(plt.gca())
    mo.vstack([
        mo.hstack([
            mo.ui.dropdown(pc_list,value=pc_list[0],label="Componente X"),
            mo.ui.dropdown(pc_list,value=pc_list[1],label="Componente Y")
        ],justify="start"),
        scores_g,
    ])
    return


@app.cell(disabled=True)
def _(loadings_df, mo, pca, plt):
    plt.figure(figsize=(6, 6))

    # Desenha as linhas dos eixos centrais
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.axvline(0, color='gray', linestyle='--', linewidth=1)

    # Plota cada vetor (loading)
    for feature in loadings_df.index:
        # Vetores vermelhos partindo da origem (0,0)
        plt.arrow(0, 0, loadings_df.loc[feature, 'PC1'], loadings_df.loc[feature, 'PC2'], 
                  color='crimson', head_width=0.04, head_length=0.04, linewidth=2, length_includes_head=True)

        # Texto identificando a variável original
        plt.text(loadings_df.loc[feature, 'PC1'] * 1.1, loadings_df.loc[feature, 'PC2'] * 1.1, 
                  feature, color='black', ha='center', va='center', fontsize=11, fontweight='bold')

    # Customização do gráfico
    plt.xlim(-1.2, 1.2)
    plt.ylim(-1.2, 1.2)
    plt.xlabel(f'Componente Principal 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)', fontsize=12)
    plt.ylabel(f'Componente Principal 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)', fontsize=12)
    plt.title('Gráfico de Cargas do PCA (PCA Loadings Plot)', fontsize=14, fontweight='bold')
    plt.gca().set_aspect('equal', adjustable='box') # Mantém a escala 1:1 correta
    loadings_g = mo.ui.matplotlib(plt.gca())
    loadings_g
    return


if __name__ == "__main__":
    app.run()
