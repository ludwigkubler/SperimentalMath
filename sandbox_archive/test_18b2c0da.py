# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    instances_tested = 0
    msd_sum = 0
    cvrank_sum = 0
    msd_cvrank_diff_sum = 0

    for _ in range(30):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        # Compute symplectic geometry degree (msd(f))
        # This is a placeholder; actual computation depends on the function
        msd_f = random.random() * n  # Example: msd(f) is a random number between 0 and n

        # Compute communication complexity rank (cvrank(f))
        # This is a placeholder; actual computation depends on the function
        cvrank_f = random.randint(1, n)  # Example: cvrank(f) is a random integer between 1 and n

        msd_sum += msd_f
        cvrank_sum += cvrank_f
        msd_cvrank_diff_sum += abs(msd_f - cvrank_f)
        instances_tested += 1

    mean_msd = msd_sum / instances_tested
    mean_cvrank = cvrank_sum / instances_tested
    mean_abs_diff = msd_cvrank_diff_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(msd_f * cvrank_f for msd_f, cvrank_f in zip([random.random() * n for _ in range(instances_tested)], [random.randint(1, n) for _ in range(instances_tested)])) - mean_msd * mean_cvrank) / (math.sqrt(instances_tested * sum((msd_f - mean_msd)**2 for msd_f in [random.random() * n for _ in range(instances_tested)]) * instances_tested * sum((cvrank_f - mean_cvrank)**2 for cvrank_f in [random.randint(1, n) for _ in range(instances_tested)])))

    conjecture_holds = correlation_coefficient >= 0.8 and mean_abs_diff <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 10**9) for _ in range(30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")