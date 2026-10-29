import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt

    return mo, np, plt


@app.cell
def _(mo):
    mo.md("""
    # Central Limit Theorem explorer

    Draw many samples of size *n* from a population, compute each sample's
    mean, and look at the histogram of those means.
    """)
    return


@app.cell
def _(mo):
    dist = mo.ui.dropdown(
        options=["Uniform(0, 1)", "Exponential(1)", "Bernoulli(0.2)"],
        value="Exponential(1)",
        label="Population",
    )
    n = mo.ui.slider(1, 100, value=5, label="Sample size n", show_value=True)
    reps = mo.ui.slider(
        200, 5000, step=200, value=2000, label="Number of samples", show_value=True
    )
    mo.hstack([dist, n, reps], justify="start", gap=2)
    return dist, n, reps


@app.cell
def _(dist, n, np, plt, reps):
    rng = np.random.default_rng(2026)
    size = (reps.value, n.value)
    if dist.value.startswith("Uniform"):
        draws, mu, sigma = rng.uniform(0, 1, size), 0.5, np.sqrt(1 / 12)
    elif dist.value.startswith("Exponential"):
        draws, mu, sigma = rng.exponential(1.0, size), 1.0, 1.0
    else:
        p = 0.2
        draws, mu, sigma = rng.binomial(1, p, size), p, np.sqrt(p * (1 - p))

    xbars = draws.mean(axis=1)
    se = sigma / np.sqrt(n.value)

    fig, ax = plt.subplots(figsize=(7, 3.8))
    ax.hist(xbars, bins=40, density=True, color="steelblue", edgecolor="white")
    grid = np.linspace(xbars.min(), xbars.max(), 300)
    ax.plot(
        grid,
        np.exp(-0.5 * ((grid - mu) / se) ** 2) / (se * np.sqrt(2 * np.pi)),
        color="crimson",
        lw=2,
        label="Normal approximation",
    )
    ax.set_xlabel(r"Sample mean $\bar{x}$")
    ax.set_ylabel("Density")
    ax.legend()
    fig.tight_layout()
    fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    The red curve is the normal distribution with mean $\mu$ and
    standard deviation $\sigma/\sqrt{n}$ predicted by the CLT.
    """)
    return


if __name__ == "__main__":
    app.run()
