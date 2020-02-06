import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
from pyprove import *
from pprint import pprint

sns.set()

PIDS = ["mzr02", "mzr02WL1_000"]

experiment = {
    "bid": "test_problems",
    "pids": PIDS,
    "limit": "T1",  # "G10000-T60"
    "cores": 4,
    "eargs": "-s --free-numbers --resources-info --print-statistics"
}


def evaluate(fig_name, experiment, ebinary="eprover"):

    experiment["ebinary"] = ebinary

    log.start("Evaluating models", experiment)

    experiment["results"] = expres.benchmarks.eval(**experiment)

    results = experiment["results"]

    pprint(results)

    runtimes = np.empty(len(results))
    processed_clauses = np.empty(len(results))
    generated_clauses = np.empty(len(results))
    status = np.empty(len(results), dtype=object)
    names = np.empty(len(results), dtype=object)
    limitation = np.empty(len(results), dtype=object)

    i = 0
    for result in results:
        if results[result]["STATUS"] != "ResourceOut":
            runtimes[i] = results[result]["RUNTIME"]
            processed_clauses[i] = results[result]["PROCESSED"]
            generated_clauses[i] = results[result]["GENERATED"]
            status[i] = results[result]["STATUS"]
            names[i] = result[1] + "__" + result[2]
            limitation[i] = result[3]
        else:
            runtimes[i] = np.nan
            processed_clauses[i] = np.nan
            generated_clauses[i] = np.nan
            status[i] = results[result]["STATUS"]
            names[i] = result[1] + "__" + result[2]
            limitation[i] = result[3]
        i += 1

    presentation_data = {
        "runtimes": runtimes,
        "processed_clauses": processed_clauses,
        "generated_clauses": generated_clauses,
        "status": status,
        "names": names,
        "limitation": limitation
    }

    presentation_df = pd.DataFrame(data=presentation_data)
    presentation_df.to_csv(
        experiment["ebinary"] + "__" + experiment["bid"] +
        str(datetime.datetime.now().isoformat()),
        sep=';',
        encoding='utf-8',
        index=False)
    line_plt = sns.lineplot(
        x="runtimes", y="processed_clauses", data=presentation_df)
    fig = line_plt.get_figure()
    fig.savefig(fig_name)


evaluate("new_version", experiment)
evaluate("original", experiment, "eprover_original")
