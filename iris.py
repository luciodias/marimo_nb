import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import matplotlib.pyplot as plt
    import pandas as pd
    from sklearn.datasets import load_iris
    from sklearn.decomposition import PCA
    from sklearn.preprocessing import StandardScaler

    # 1. Load a sample dataset (Iris dataset has 4 features)
    iris = load_iris()
    X = iris.data
    y = iris.target
    feature_names = iris.feature_names

    print(X)

    # 2. Standardize the data (Crucial step for PCA)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print(X_scaled)

    # 3. Instantiate and fit PCA (reducing from 4 features to 2)
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    # 4. Check how much information (variance) was retained
    print(
        f"Explained variance ratio per component: {pca.explained_variance_ratio_}"
    )
    print(f"Total variance retained: {sum(pca.explained_variance_ratio_):.2%}")

    # 5. Plot the 2D projected data
    plt.figure(figsize=(8, 6))
    colors = ["navy", "turquoise", "darkorange"]
    for color, i, target_name in zip(colors, [0, 1, 2], iris.target_names):
        plt.scatter(
            X_pca[y == i, 0],
            X_pca[y == i, 1],
            color=color,
            alpha=0.8,
            lw=2,
            label=target_name,
        )

    plt.legend(loc="best", shadow=False, scatterpoints=1)
    plt.title("PCA of IRIS dataset")
    plt.xlabel("Principal Component 1")
    plt.ylabel("Principal Component 2")
    plt.grid(True)
    plt.show()

    return


if __name__ == "__main__":
    app.run()
