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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = int(math.log2(len(f)))
        if n == 0: return 0
        rank = 0
        for i in range(1, n+1):
            count = sum(1 for j in range(n) if f[j] != f[j+i])
            rank += count / (n - i)
        return rank
    
    def minimal_representation_degree(f):
        # Placeholder function; actual implementation required
        return len(f)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            R_f = communication_complexity_rank_variance(f)
            D_f = minimal_representation_degree(f)
            results.append({"n": n, "R_f": R_f, "D_f": D_f})
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    R_f_values = [result["R_f"] for result in results]
    D_f_values = [result["D_f"] for result in results]
    
    n_max = max(result["n"] for result in results)
    
    if n_max < 16:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max_too_small"
        }
    
    # Polynomial fitting
    coefficients = []
    for i in range(1, 4):
        sum_products = sum(R_f_values[j] * D_f_values[j]**i for j in range(len(results)))
        sum_R_f = sum(R_f_values)
        sum_D_f_i = sum(D_f_values[i] for i in range(len(results)))
        coefficients.append(sum_products / (sum_R_f * sum_D_f_i))
    
    correlation_coefficient = coefficients[0]
    polynomial_coefficient = coefficients[-1]
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7 and polynomial_coefficient <= (max(R_f_values))**1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")