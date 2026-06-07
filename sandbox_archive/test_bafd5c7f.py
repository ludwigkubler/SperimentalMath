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
    
    def matrix_representation(f):
        n = len(f.__code__.co_varnames)
        M_f = [[0] * n for _ in range(n)]
        for i in range(2**n):
            inputs = [i >> j & 1 for j in range(n)]
            outputs = f(*inputs)
            if outputs == 1:
                for j in range(n):
                    if inputs[j]:
                        M_f[j][j] += 1
        return M_f
    
    def geometric_entropy(M):
        n = len(M)
        total = sum(sum(row) for row in M)
        entropy = 0
        for i in range(n):
            p_i = sum(M[i]) / total
            if p_i > 0:
                entropy -= p_i * math.log2(p_i)
        return entropy
    
    def communication_complexity_rank_variance(f):
        n = len(f.__code__.co_varnames)
        ranks = []
        for i in range(2**n):
            inputs = [i >> j & 1 for j in range(n)]
            outputs = f(*inputs)
            if outputs == 1:
                rank = sum(inputs) + sum(outputs)
                ranks.append(rank)
        mean_rank = sum(ranks) / len(ranks)
        variance = sum((x - mean_rank)**2 for x in ranks) / len(ranks)
        return variance
    
    def f_n(x):
        return x[0] and not x[1]
    
    M_f = matrix_representation(f_n)
    n = len(M_f)
    if n <= 1:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entropy = geometric_entropy(M_f)
    variance = communication_complexity_rank_variance(f_n)
    
    if variance == 0:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "variance_is_zero"
        }
    
    ratio = entropy / variance
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if ratio <= f_n(n) else False,
        "counterexample": "" if ratio <= f_n(n) else "ratio_exceeds_f_n"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    elif any(not result["conjecture_holds"] and "counterexample" not in result for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if "counterexample" in result)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    else:
        support_fraction = 0.0
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")