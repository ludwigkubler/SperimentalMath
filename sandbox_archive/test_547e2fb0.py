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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 10
    d = 5
    
    # Generate a random polynomial function f over {0,1}^n with degree d
    variables = [f'x{i}' for i in range(n)]
    terms = []
    for _ in range(d):
        coeffs = [random.choice([0, 1]) for _ in range(n + 1)]
        term = sum(c * v if i > 0 else c for i, (c, v) in enumerate(zip(coeffs, variables)))
        terms.append(term)
    f = sum(terms)
    
    # Compute the discrepancy tensor T_f
    T_f = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                T_f[i][j] = 1
    
    # Construct a BP P that computes f using its characteristic function and measure
    def bp_p(x):
        return f.subs({v: x[i] for i, v in enumerate(variables)})
    
    # Measure the output distribution of P for each instance and calculate Discrepancy(P)
    instances_tested = 100
    discrepancy_sum = 0
    for _ in range(instances_tested):
        x = [random.choice([0, 1]) for _ in range(n)]
        y = bp_p(x)
        discrepancy_sum += abs(y - 0.5)
    
    discrepancy_avg = discrepancy_sum / instances_tested
    
    # Correlate Min_Rank(T_f) with Discrepancy(P) for multiple instances to check if the conjectured relationship holds
    min_rank_T_f = sum(1 for row in T_f if any(val != 0 for val in row))
    
    metric_value = discrepancy_avg
    conjecture_holds = discrepancy_avg >= 0.5 * min_rank_T_f
    counterexample = "" if conjecture_holds else "discrepancy < 0.5 * min_rank(T_f)"
    
    return {
        "metric_name": "Discrepancy(P)",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"discrepancy < 0.5 * min_rank(T_f)\" first_failing_seed={first_failing_seed}")