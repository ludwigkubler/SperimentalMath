# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i, n):
                A[i][j] /= pivot
            for k in range(n):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(i, n):
                        A[k][j] -= factor * A[i][j]
        return A

    def characteristic_polynomial(F, p):
        n = len(F)
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    A[i][j] += Fraction(-1)
                else:
                    A[i][j] += Fraction(F[i][j], p)
        A = gaussian_elimination(A)
        det = 1
        for i in range(n):
            det *= A[i][i]
        return det

    def clause_complexity(F):
        m = len(F)
        return m

    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    
    for n in n_values:
        F = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        p = random.choice([2, 3, 5, 7, 11])
        v_p = characteristic_polynomial(F, p)
        c_F = clause_complexity(F)
        metrics.append({
            "n": n,
            "v_p": v_p,
            "c_F": c_F
        })
    
    if not metrics:
        return {
            "metric_name": "min_v_p",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_metrics_collected"
        }
    
    min_v_p = min(metric["v_p"] for metric in metrics)
    mean_c_F = sum(metric["c_F"] for metric in metrics) / len(metrics)
    std_dev_c_F = math.sqrt(sum((metric["c_F"] - mean_c_F) ** 2 for metric in metrics) / len(metrics))
    
    return {
        "metric_name": "min_v_p",
        "metric_value": min_v_p,
        "instances_tested": len(metrics),
        "n_max": max(metric["n"] for metric in metrics),
        "conjecture_holds": False,
        "counterexample": "not_computed"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results_collected")
        sys.exit(0)
    
    mean_min_v_p = sum(r["metric_value"] for r in results) / len(results)
    std_dev_min_v_p = math.sqrt(sum((r["metric_value"] - mean_min_v_p) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_min_v_p} std={std_dev_min_v_p} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "not_computed" for r in results):
        counterexamples = [r["counterexample"] for r in results if r["counterexample"] != "not_computed"]
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "not_computed")
        print(f"RESULT: FALSIFIED counterexample=\"{' '.join(counterexamples)}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE not_enough_supporting_evidence")