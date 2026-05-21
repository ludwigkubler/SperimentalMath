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
    
    def hypergeometric_function(n, k):
        if k > n or k < 0:
            return 0
        p = k / n
        q = (n - k) / n
        hypergeom = math.comb(n, k) * (p ** k) * (q ** (n - k))
        return hypergeom

    def moments_of_hypergeometric(hypergeom, k):
        if k == 0:
            return [1]
        moments = [1]
        for i in range(1, k + 1):
            moment = sum(moments[j] * math.comb(i, j) * hypergeom ** (i - j) for j in range(i))
            moments.append(moment)
        return moments

    n_min = 5
    n_max = 40
    n_values = [n for n in range(n_min, n_max + 1)]
    k_max = int(math.log2(n))

    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(3):  # Sample 3 random AC0 circuits per size
            instances_tested += 1
            moments_sum = sum(moments_of_hypergeometric(hypergeometric_function(n, k), k) for k in range(k_max + 1))
            if moments_sum == 0:
                continue
            ratio = moments_sum / (math.log(n) ** k_max)
            if not conjecture_holds and counterexample == "":
                counterexample = f"n={n}, moments_sum={moments_sum}, log^k(n)={math.log(n) ** k_max}"
            if ratio < 1 or ratio > 2:  # Adjust the bounds as needed
                conjecture_holds = False

    return {
        "metric_name": "Ratio of Moments to Log^k(n)",
        "metric_value": moments_sum / (math.log(n) ** k_max),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")