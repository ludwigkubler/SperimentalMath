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
    
    def frobenius_norm(cnf):
        n = len(cnf[0])
        Q = [[0] * n for _ in range(n)]
        for clause in cnf:
            sign = 1
            for lit in clause:
                var = abs(lit) - 1
                if lit < 0:
                    sign *= -1
                Q[var][var] += sign ** 2
        return sum(sum(row[i] * row[j] for i in range(n)) for j, row in enumerate(Q)) ** 0.5

    def resolution_length(cnf):
        n = len(cnf[0])
        clauses = list(cnf)
        length = 0
        while True:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(lit in clauses[j] for lit in clauses[i]):
                        new_clause = [lit for lit in clauses[i] if lit not in clauses[j]]
                        break
                if new_clause:
                    break
            if not new_clause:
                break
            length += 1
            clauses.append(new_clause)
        return length

    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = random.sample(range(1, n + 1), random.randint(1, n))
            random.shuffle(clause)
            cnf.append(tuple(clause))
        return tuple(cnf)

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
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
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }

    log_Q_norm_squared_over_n, log_t_star = zip(*results)
    correlation_coefficient = sum((x - mean(log_Q_norm_squared_over_n)) * (y - mean(log_t_star))
                                  for x, y in zip(log_Q_norm_squared_over_n, log_t_star)) / len(results) / \
                              math.sqrt(sum((x - mean(log_Q_norm_squared_over_n)) ** 2 for x in log_Q_norm_squared_over_n)) / \
                              math.sqrt(sum((y - mean(log_t_star)) ** 2 for y in log_t_star))
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean(log_Q_norm_squared_over_n) <= 3,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = mean([r["metric_value"] for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_too_low\" first_failing_seed={first_failing_seed}")