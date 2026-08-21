import marimo

__generated_with = "0.23.16"
app = marimo.App(width="full")


@app.cell
def _():
    import re

    import marimo as mo
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.decomposition import PCA

    return PCA, mo, np, pd, plt, re


@app.cell
def cell_load_data(pd, re):
    """Load CSV data - reads only needed columns, not entire file into context.

    The CSV is semicolon-delimited. Each oil type contributes 3 contiguous
    columns: an average plus two samples (suffix 1 / 2). The average is the
    first column of each oil group and is used as the PCA feature. Headers may
    contain non-breaking spaces, so whitespace is normalized before grouping.
    """
    df = pd.read_csv("raman/spectra_oleos_comestiveis.csv", sep=",", header=0)
    data_cols = df.iloc[:, 1:]  # skip R.Shift column

    # Normalize whitespace (handles non-breaking spaces U+00A0 in headers)
    def _norm(s):
        return re.sub(r"\s+", " ", str(s)).strip()

    norm_cols = [_norm(c) for c in data_cols.columns]

    # Recover the base oil name: drop " media" (and any surrounding spaces),
    # then drop a trailing sample digit (1 / 2). Keep the first occurrence of
    # each base, which is the average column.
    def _base(name):
        n = re.sub(r"\s*media\s*", "", name)
        n = re.sub(r"[12]$", "", n)
        return n.strip()

    bases = [_base(c) for c in norm_cols]
    seen = set()
    avg_idx = []
    for i, b in enumerate(bases):
        if b and b not in seen:
            seen.add(b)
            avg_idx.append(i)

    X = data_cols.iloc[:, avg_idx].values.astype(float)
    avg_cols = [data_cols.columns[i] for i in avg_idx]
    return X, avg_cols


@app.cell
def cell_pca_analysis(PCA, X):
    """Perform PCA on the centered data."""
    X_centered = X - X.mean(axis=0)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_centered)
    explained_var = pca.explained_variance_ratio_
    return X_pca, explained_var


@app.cell
def cell_create_results(X_pca, explained_var, pd, plt):
    """Create results DataFrame and scatter-plot figure."""
    results = pd.DataFrame({
        "PC1": X_pca[:, 0],
        "PC2": X_pca[:, 1],
    })

    fig, ax = plt.subplots()
    ax.scatter(X_pca[:, 0], X_pca[:, 1], alpha=0.6)
    ax.set_xlabel(f"PC1 ({explained_var[0]:.2%} variance)")
    ax.set_ylabel(f"PC2 ({explained_var[1]:.2%} variance)")
    ax.set_title("PCA of Oleos Comestiveis Spectra")
    plt.tight_layout()

    return fig, results


@app.cell
def _(cell_create_results, cell_load_data, cell_pca_analysis, mo):
    X, avg_cols = cell_load_data()
    X_pca, explained_var = cell_pca_analysis(X)
    fig, results = cell_create_results(X_pca, explained_var)

    mo.md(
        f"""
        ## PCA of Oleos Comestiveis Spectra

        Features used ({len(avg_cols)} average spectra): {', '.join(map(str, avg_cols))}

        - **PC1** explains {explained_var[0]:.2%} of variance
        - **PC2** explains {explained_var[1]:.2%} of variance
        - **Total** explained: {explained_var.sum():.2%}
        """
    )
    fig
    results
    return (fig, results, avg_cols, X, X_pca, explained_var)


if __name__ == "__main__":
    app.run()
