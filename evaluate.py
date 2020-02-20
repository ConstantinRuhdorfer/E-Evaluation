# import seaborn as sns
import pandas as pd
import numpy as np
# import matplotlib.pyplot as plt
import datetime
from pyprove import *
from pprint import pprint

# sns.set()

PIDS = ["mzr02WL10_000FP2", "mzr02WL10_000FP4", "mzr02WL10_000FP6",
        "mzr02WL10_000FP8", "mzr02WL10_000FP10", "mzr02WL10_000NoIndex"]

# PIDS = ["mzr02WL10_000FP8", "mzr02WL10_000NoIndex"]

experiment = {
    "bid": "mizar40-tenth",
    "pids": PIDS,
    "limit": "G10000-T720",  # "G10000-T60"
    "cores": 24,
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
    strategy = np.empty(len(results), dtype=object)
    names = np.empty(len(results), dtype=object)
    limitation = np.empty(len(results), dtype=object)
    c_p_c = np.empty(len(results), dtype=object)
    c_p_p_o_c  = np.empty(len(results), dtype=object)
    c_p_p_n_o_c  = np.empty(len(results), dtype=object)
    c_p_n_uc  = np.empty(len(results), dtype=object)
    c_p_non_uc  = np.empty(len(results), dtype=object)

    i = 0
    for result in results:
        if "RUNTIME" in results[result]:
            runtimes[i] = results[result]["RUNTIME"]
        else:
            runtimes[i] = 720
        if "PROCESSED" in results[result]:
            processed_clauses[i] = results[result]["PROCESSED"]
        else:
            processed_clauses[i] = np.nan
        if "GENERATED" in results[result]:
            generated_clauses[i] = results[result]["GENERATED"]
        else:
            generated_clauses[i] = np.nan
        if "CURR_PROCESSED_CLAUSES" in results[result]:
            c_p_c[i] = results[result]["CURR_PROCESSED_CLAUSES"]
        else:
            c_p_c[i] = np.nan
        if "CURR_PROCESSED_POS_OR_UC" in results[result]:
            c_p_p_o_c[i] = results[result]["CURR_PROCESSED_POS_OR_UC"]
        else:
            c_p_p_o_c[i] = np.nan
        if "CURR_PROCESSED_POS_NOT_OR_UC" in results[result]:
            c_p_p_n_o_c[i] = results[result]["CURR_PROCESSED_POS_NOT_OR_UC"]
        else:
            c_p_p_n_o_c[i] = np.nan
        if "CURR_PROCESSED_NEG_UC" in results[result]:
            c_p_n_uc[i] = results[result]["CURR_PROCESSED_NEG_UC"]
        else:
            c_p_n_uc[i] = np.nan
        if "CURR_PROCESSED_NON_UC" in results[result]:
            c_p_non_uc[i] = results[result]["CURR_PROCESSED_NON_UC"]
        else:
            c_p_non_uc[i] = np.nan 
        status[i] = results[result]["STATUS"]
        strategy[i] = result[1]
        names[i] = result[2]
        limitation[i] = result[3]
        i += 1

    presentation_data = {
        "runtimes": runtimes,
        "processed_clauses": processed_clauses,
        "generated_clauses": generated_clauses,
        "status": status,
        "strategy": strategy,
        "names": names,
        "limitation": limitation,
        "CURR_PROCESSED_CLAUSES": c_p_c,
        "CURR_PROCESSED_POS_OR_UC": c_p_p_o_c,
        "CURR_PROCESSED_POS_NOT_OR_UC": c_p_p_n_o_c,
        "CURR_PROCESSED_NEG_UC": c_p_n_uc,
        "CURR_PROCESSED_NON_UC": c_p_non_uc
    }

    presentation_df = pd.DataFrame(data=presentation_data)
    presentation_df.to_csv(
        experiment["ebinary"] + "__" + experiment["bid"] +
        str(datetime.datetime.now().isoformat()),
        sep=';',
        encoding='utf-8',
        index=False)
    # line_plt = sns.lineplot(
    #     x="runtimes", y="processed_clauses", data=presentation_df)
    # fig = line_plt.get_figure()
    # fig.savefig(fig_name)


evaluate("new_version", experiment, "/local1/constantinr/cr_eprover/PROVER/eprover")
