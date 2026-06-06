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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
                clause[1] *= -1
            cnf.append(clause)
        return cnf
    
    def min_symmetric_bilinear_form(cnf):
        n = max(abs(x) for x in sum(cnf, []))
        form = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            i, j = abs(clause[0]), abs(clause[1])
            sign_i = -1 if clause[0] < 0 else 1
            sign_j = -1 if clause[1] < 0 else 1
            form[i][j] += sign_i * sign_j
        return sum(sum(row) for row in form)
    
    def communication_complexity_rank_variance(cnf):
        n = max(abs(x) for x in sum(cnf, []))
        rank = 0
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if any(clause[i] * clause[j] < 0 for clause in cnf):
                    rank += 1
        return rank
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x_i - mean_x) * (y_i - mean_y) for x_i, y_i in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((x_i - mean_x) ** 2 for x_i in x) / len(x))
        std_y = math.sqrt(sum((y_i - mean_y) ** 2 for y_i in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        min_sbf_values = []
        ccr_var_values = []
        for _ in range(30):
            cnf = generate_cnf(n, random.randint(2 * n, 3 * n))
            min_sbf_values.append(min_symmetric_bilinear_form(cnf))
            ccr_var_values.append(communication_complexity_rank_variance(cnf))
        
        correlation = correlation_coefficient(min_sbf_values, ccr_var_values)
        results.append({
            "n": n,
            "min_sbf_mean": sum(min_sbf_values) / len(min_sbf_values),
            "ccr_var_mean": sum(ccr_var_values) / len(ccr_var_values),
            "correlation_coefficient": correlation
        })
    
    mean_metric_value = sum(result["correlation_coefficient"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["correlation_coefficient"]) >= 0.5) / len(results)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": mean_metric_value,
        "instances_tested": 30 * len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"Correlation < 0.5 at n={results[support_fraction == 0]['n']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")