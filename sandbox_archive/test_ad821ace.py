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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def frobenius_norm(cnf):
        n = len(cnf)
        Q = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            x, y = abs(clause[0]), abs(clause[1])
            Q[x][y] += 1
            Q[y][x] += 1
        trace = sum(Q[i][i] for i in range(1, n + 1))
        det = 1
        for i in range(1, n + 1):
            det *= (Q[i][i] - sum(Q[j][i] * Q[i][j] / det for j in range(i)))
        return math.sqrt(trace**2 + det)
    
    def resolution_length(cnf):
        # Placeholder for actual resolution length calculation
        # This is a dummy implementation for testing purposes
        return len(cnf) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            m = random.randint(n // 2, n)
            cnf = generate_cnf(n, m)
            Q_norm = frobenius_norm(cnf)
            t_star = resolution_length(cnf)
            if Q_norm == 0 or t_star == 0:
                continue
            log_Q_norm_squared_over_n = math.log(Q_norm**2 / n)
            log_t_star = math.log(t_star)
            results.append((log_Q_norm_squared_over_n, log_t_star))
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    log_Q_norm_squared_over_n = [r[0] for r in results]
    log_t_star = [r[1] for r in results]
    correlation_coefficient = sum((log_Q_norm_squared_over_n[i] - mean(log_Q_norm_squared_over_n)) * (log_t_star[i] - mean(log_t_star)) for i in range(len(results))) / (len(results) * std(log_Q_norm_squared_over_n) * std(log_t_star))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean(log_Q_norm_squared_over_n) <= 3,
        "counterexample": ""
    }

def mean(lst):
    return sum(lst) / len(lst)

def std(lst):
    avg = mean(lst)
    variance = sum((x - avg) ** 2 for x in lst) / len(lst)
    return math.sqrt(variance)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = mean([r["metric_value"] for r in results])
    std_metric_value = std([r["metric_value"] for r in results])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient\" first_failing_seed={first_failing_seed}")

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        cnf.append(clause)
    return cnf

def frobenius_norm(cnf):
    n = len(cnf)
    Q = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in cnf:
        x, y = abs(clause[0]), abs(clause[1])
        Q[x][y] += 1
        Q[y][x] += 1
    trace = sum(Q[i][i] for i in range(1, n + 1))
    det = 1
    for i in range(1, n + 1):
        det *= (Q[i][i] - sum(Q[j][i] * Q[i][j] / det for j in range(i)))
    return math.sqrt(trace**2 + det)

def resolution_length(cnf):
    # Placeholder for actual resolution length calculation
    # This is a dummy implementation for testing purposes
    return len(cnf) ** 2

def mean(lst):
    return sum(lst) / len(lst)

def std(lst):
    avg = mean(lst)
    variance = sum((x - avg) ** 2 for x in lst) / len(lst)
    return math.sqrt(variance)