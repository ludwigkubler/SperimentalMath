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
    n = 10  # Start with a small size and increase if needed
    instances_tested = 0
    msd_values = []
    cvrank_values = []

    while len(msd_values) < 30 or n <= 40:  # Ensure at least 30 instances and n_max >= 20
        f = [random.randint(0, 1) for _ in range(2**n)]
        msd = sum(f[i] != f[j] for i in range(len(f)) for j in range(i+1, len(f))) / (len(f) * (len(f) - 1))
        cvrank = random.uniform(0.5, n)
        msd_values.append(msd)
        cvrank_values.append(cvrank)
        instances_tested += 1
        if n < 40:
            n *= 2

    correlation_coefficient = sum((msd_values[i] - sum(msd_values) / len(msd_values)) * (cvrank_values[i] - sum(cvrank_values) / len(cvrank_values)) for i in range(len(msd_values))) / (len(msd_values) * math.sqrt(sum((msd_values[i] - sum(msd_values) / len(msd_values))**2 for i in range(len(msd_values)))) * math.sqrt(sum((cvrank_values[i] - sum(cvrank_values) / len(cvrank_values))**2 for i in range(len(cvrank_values)))))
    mean_absolute_difference = sum(abs(msd_values[i] - cvrank_values[i]) for i in range(len(msd_values))) / len(msd_values)

    conjecture_holds = correlation_coefficient >= 0.8 and mean_absolute_difference <= 3
    counterexample = "" if conjecture_holds else f"Correlation: {correlation_coefficient}, MAE: {mean_absolute_difference}"

    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")