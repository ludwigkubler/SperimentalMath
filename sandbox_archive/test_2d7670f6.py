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
    
    def generate_disjointness_matrix(n):
        X = [set(range(i, i + n)) for i in range(0, n * n, n)]
        Y = [set(range(i, i + n)) for i in range(0, n * n, n)]
        M = [[random.choice([0, 1]) if x.isdisjoint(y) else 0 for y in Y] for x in X]
        return M
    
    def matrix_norm(M):
        norm = 0
        for row in M:
            for val in row:
                norm += abs(val)
        return norm
    
    n_values = [10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        M = generate_disjointness_matrix(n)
        norm = matrix_norm(M)
        tau_M = math.log(norm) - math.log(n) - math.log(n)
        results.append({"n": n, "tau_M": tau_M})
    
    metric_name = "disjointness_communication_complexity"
    instances_tested = len(results)
    conjecture_holds = all(result["tau_M"] >= 0.5 * math.sqrt(result["n"]) for result in results)
    counterexample = "" if conjecture_holds else f"Graph with n={results[0]['n']}, tau_M={results[0]['tau_M']}"
    
    return {
        "metric_name": metric_name,
        "metric_value": sum(result["tau_M"] for result in results) / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")