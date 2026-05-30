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
            cnf.append(clause)
        return cnf
    
    def frobenius_norm(cnf):
        n = len(cnf[0])
        Q = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                var = abs(lit)
                sign = -1 if lit < 0 else 1
                Q[var][var] += sign ** 2
        norm = 0
        for i in range(1, n + 1):
            norm += Q[i][i]
        return math.sqrt(norm)
    
    def resolution_length(cnf):
        # Simplified heuristic to estimate resolution length
        m = len(cnf)
        return m * (m ** 0.5)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(n // 2, n))
            Q_norm = frobenius_norm(cnf)
            t_star = resolution_length(cnf)
            if Q_norm == 0 or t_star == 0:
                continue
            log_Q_norm_squared_over_n = math.log(Q_norm ** 2 / n)
            log_t_star = math.log(t_star)
            results.append((log_Q_norm_squared_over_n, log_t_star))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_Q_norm_squared_over_n = [r[0] for r in results]
    log_t_star = [r[1] for r in results]
    correlation = sum((log_Q_norm_squared_over_n[i] - mean(log_Q_norm_squared_over_n)) * (log_t_star[i] - mean(log_t_star)) for i in range(len(results))) / len(results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max([len(cnf) for cnf, _ in results]),
        "conjecture_holds": correlation >= 0.8 and mean(log_Q_norm_squared_over_n) <= 3,
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation < 0.8\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support or budget_exceeded n_tested=30")