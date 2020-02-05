import matplotlib.pyplot as plt
from pyprove import *
from pprint import pprint

import numpy as np
import pandas as pd

import seaborn as sns
sns.set()

PIDS = ["mzr02"]

experiment = {
    "bid": "test_problems",
    "pids": PIDS,
    "limit": "T1",  # "G10000-T60"
    "cores": 4,
    "eargs": "-s --free-numbers"
}


def evaluate(fig_name, experiment, ebinary="eprover"):

    experiment["ebinary"] = ebinary

    log.start("Evaluating models", experiment)

    experiment["results"] = expres.benchmarks.eval(**experiment)

    results = experiment["results"]

    runtimes = np.empty(len(results))
    processed_clauses = np.empty(len(results))

    i = 0
    for result in results:
        runtimes[i] = results[result]["RUNTIME"]
        processed_clauses[i] = results[result]["PROCESSED"]
        i += 1

    presentation_data = {
        "runtimes": runtimes,
        "processed_clauses": processed_clauses
    }

    presentation_df = pd.DataFrame(data=presentation_data)
    line_plt = sns.lineplot(
        x="runtimes", y="processed_clauses", data=presentation_df)
    fig = line_plt.get_figure()
    fig.savefig(fig_name)


evaluate("new_version", experiment)
evaluate("original", experiment, "eprover_original")
