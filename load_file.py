import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    mo.ui.file_browser(
        selection_mode="file",
        multiple=False,
        ignore_empty_dirs=True,
    )
    return (mo,)


@app.cell
def _(mo):
    mo.ui.file(
        filetypes=['.csv'],
    )
    return


@app.cell
def _(mo):
    mo.ui.data_editor(data=[1,2,3])
    return


if __name__ == "__main__":
    app.run()
