from datetime import datetime
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as sps
import seaborn as sns
from loguru import logger
from scipy import stats as scs


def central_limit(presets, n: int):
    samples = []
    # for every combination of mean and standard deviation
    for mu, sd in zip(presets.mu, presets.sd):
        # sample a normal distribution
        samples.append(sps.norm(loc=mu, scale=sd).rvs(1000))
    # and gather in a dataframe
    data = pd.DataFrame(samples).T.melt()

    # create a square grid
    grid = int(np.ceil(np.sqrt(n)))
    fig, axs = plt.subplots(
        grid, grid, figsize=presets.figsize, constrained_layout=True
    )
    axs = axs.ravel()

    # take a first sample of 100 items from the population
    draw = np.array(data.sample(n=100).value)
    # and plot
    sns.kdeplot(x=draw, ax=axs[0])
    axs[0].set_title(f"sample #0")

    for i in range(1, n):
        # keep sampling and add the sample to the previous one
        draw += np.array(data.sample(n=100).value)
        sns.kdeplot(x=draw, ax=axs[i])
        axs[i].set_title(f"sample #{i}")
        axs[i].set_ylabel("")

    # titles
    fig.suptitle("Central Limit Theorem")
    fig.supylabel("Density")

    # save file
    filename = presets.imagedir / (datetime.now().strftime("%Y%m%d-%H%M") + ".png")
    plt.savefig(filename)
    logger.info(f"Saved file to {filename}")


def simulate_simpson(presets):
    groups = presets.groups
    difference = presets.difference
    slope = presets.slope
    var = presets.var
    rng = np.random.default_rng(1)
    data: List = []
    # for every group
    for i in range(groups):
        # draw some random numbers, scaled by var
        x = rng.random(n) * var
        # and make a linear relation
        y = slope * x + rng.random(n)
        # and move the group a difference amount
        data.append([x + difference * i, y + difference * (i * -np.sign(slope))])

    # gather everything from the list of lists
    x = np.concatenate([x for (x, y) in data])
    y = np.concatenate([y for (x, y) in data])

    # add group labels
    g = range(len(data))
    n = len(x) / len(data)
    groups = np.repeat(g, n)
    # and put in a dataframe
    df = pd.DataFrame({"x": x, "y": y, "group": groups})

    # plot all groups
    sns.lmplot(data=df, x="x", y="y", ci=99)
    filename = presets.imagedir / (
        "all_ " + datetime.now().strftime("%Y%m%d-%H%M") + ".png"
    )
    plt.savefig(filename)
    logger.info(f"Saved file to {filename}")

    # plot all subgroups
    sns.lmplot(data=df, x="x", y="y", hue="group", ci=99)
    filename = presets.imagedir / (
        "sub_" + datetime.now().strftime("%Y%m%d-%H%M") + ".png"
    )
    plt.savefig(filename)
    logger.info(f"Saved file to {filename}")


def beta_examples(presets):

    fix, axs = plt.subplots(presets.subs[0], presets.subs[1], figsize=presets.figsize)
    axs = axs.ravel()

    for i, ab in enumerate(presets.pairs):
        beta = scs.beta(ab[0], ab[1])
        x = np.linspace(0, 1, 100)
        y = beta.pdf(x)
        axs[i].plot(x, y)
        axs[i].set_title(f"Beta {ab}")
    plt.tight_layout()
    filename = presets.imagedir / (
        "beta_" + datetime.now().strftime("%Y%m%d-%H%M") + ".png"
    )
    plt.savefig(filename)
    logger.info(f"Saved file to {filename}")
