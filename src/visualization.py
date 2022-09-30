import matplotlib.pyplot as plt
import seaborn as sns
from fitter import Fitter, get_common_distributions
from scipy import stats as scs
from sklearn.inspection import DecisionBoundaryDisplay
from sklearn.model_selection import train_test_split


def custom_summary(f: Fitter, ax, nbest: int = 5):
    best = list(f.get_best().keys())[0]  # name of best fit

    # construct a title with the parameters
    title = f"{best} | "
    for (k, v) in f.get_best()[best].items():
        # .items() returen (key, value) pairs
        # key is the name of the parameter
        # value is a floating point.
        # with :.3f we format the floating points to 3 digits accuracy

        title = title + k + " : "
        title = title + f"{v:.3f}" + " | "
    # it is cleaner to get rid of the last two characters "| "
    title = title[:-2]

    # plot the histogram
    ax.hist(f._data, bins=30, density=True)
    # sort the top n names of distributions
    names = list(f.df_errors.sort_values(by="sumsquare_error").index)[:nbest]
    # plot every distribution
    for name in names:
        ax.plot(f.x, f.fitted_pdf[name], label=name)
    ax.set_title(title)
    ax.legend()


def test_distribution(x):
    fig, axs = plt.subplots(1, 2, figsize=(12, 6))
    d = get_common_distributions()
    f = Fitter(x, distributions=d)
    f.fit()

    custom_summary(f, axs[0])
    scs.probplot(x, dist="norm", plot=axs[1])
    fig.show()
    return f


def inspect_model(model, X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model.fit(X_train, y_train)
    disp = DecisionBoundaryDisplay.from_estimator(model, X, alpha=0.4)
    sns.scatterplot(x=X.iloc[:, 0], y=X.iloc[:, 1], hue=y, ax=disp.ax_)
