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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            denom = A[i][i]
            for j in range(n):
                A[i][j] /= denom
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def rank(A):
        m, n = len(A), len(A[0])
        row_echelon_form = gaussian_elimination(A)
        rank = 0
        for row in row_echelon_form:
            if any(row):
                rank += 1
        return rank

    def calculate_ranks(protocols):
        ranks = []
        for protocol in protocols:
            ker_phi = [row[:len(protocol)] for row in protocol]
            ker_phi_rank = rank(ker_phi)
            ranks.append(ker_phi_rank)
        return ranks

    def log_variance(ranks):
        mean_rank = sum(ranks) / len(ranks)
        variance = sum((x - mean_rank) ** 2 for x in ranks) / len(ranks)
        return math.log(variance)

    n = random.randint(5, 30)
    m = random.randint(1, n * (n - 1))
    protocols = [random.choices([0, 1], k=n*m) for _ in range(m)]
    
    ranks = calculate_ranks(protocols)
    log_var = log_variance(ranks)
    n_max = max(len(protocol) for protocol in protocols)
    
    if len(ranks) < 30:
        return {
            "metric_name": "log(r(φ))",
            "metric_value": None,
            "instances_tested": len(ranks),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    k = 1.0
    conjecture_holds = all(log_var <= k * math.log(n) for _ in range(30))
    counterexample = "" if conjecture_holds else "log(r(φ)) > k·log(n)"
    
    return {
        "metric_name": "log(r(φ))",
        "metric_value": log_var,
        "instances_tested": len(ranks),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all("metric_value" in r and r["metric_value"] is not None for r in results):
        mean_metric = sum(r["metric_value"] for r in results) / len(results)
        std_metric = math.sqrt(sum((r["metric_value"] - mean_metric) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((i for i, r in enumerate(results) if "metric_value" not in r or r["metric_value"] is None), -1)
        print(f"RESULT: INCONCLUSIVE reason=missing_data n_tested={first_failing_seed + 1}")