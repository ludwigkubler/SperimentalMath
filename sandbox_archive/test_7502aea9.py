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
    
    def xor_tautology(n):
        return [random.randint(0, 1) for _ in range(n)]
    
    def tropical_derivative(tau):
        n = len(tau)
        D = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if tau[i] != tau[j]:
                    D[i][j] = 1
        return D
    
    def resolution_length(tau):
        n = len(tau)
        clauses = [tau]
        while True:
            new_clauses = []
            for i in range(n):
                for j in range(i + 1, n):
                    if tau[i] != tau[j]:
                        new_clause = [1 - tau[i], 1 - tau[j]]
                        if new_clause not in clauses and new_clause[::-1] not in clauses:
                            new_clauses.append(new_clause)
            if len(new_clauses) == len(clauses):
                return len(clauses)
            clauses.extend(new_clauses)
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        sorted_x = sorted(range(n), key=lambda i: x[i])
        sorted_y = sorted(range(n), key=lambda i: y[i])
        rank_x = [sorted_x.index(i) for i in range(n)]
        rank_y = [sorted_y.index(i) for i in range(n)]
        n = len(x)
        sum_diff_squared = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squared) / (n * (n**2 - 1))
    
    def polynomial_regression(x, y):
        n = len(x)
        x_sum = sum(x)
        y_sum = sum(y)
        xy_sum = sum(xi * yi for xi, yi in zip(x, y))
        xx_sum = sum(xi ** 2 for xi in x)
        a = (n * xy_sum - x_sum * y_sum) / (n * xx_sum - x_sum ** 2)
        b = (y_sum - a * x_sum) / n
        return a, b
    
    def theta_log_n(n, epsilon):
        return epsilon * math.log(n)
    
    results = []
    for _ in range(30):
        n = random.randint(4, 40)
        tau = xor_tautology(n)
        D = tropical_derivative(tau)
        r = resolution_length(tau)
        results.append((D, r))
    
    correlation_values = [spearman_rank_correlation([D for D, _ in results], [r for _, r in results])]
    a, b = polynomial_regression(range(4, 41), correlation_values)
    g_n_epsilon = lambda n, epsilon: abs(a * n + b) - theta_log_n(n, epsilon)
    
    if all(correlation > 0.7 for correlation in correlation_values):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Spearman rank correlation not above 0.7"
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": sum(correlation_values) / len(correlation_values),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 10**9) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation not above 0.7\" first_failing_seed={first_failing_seed}")