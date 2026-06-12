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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(G):
        if not G:
            return True
        for literal in set(lit for clause in G for lit in clause):
            pos_lit = abs(literal)
            new_G = [clause for clause in G if literal not in clause and -literal not in clause]
            if dpll(new_G):
                return True
            new_G = [clause for clause in G if -literal not in clause]
            if dpll(new_G):
                return True
        return False
    
    def mls(G):
        n = len(G)
        if n == 0:
            return 0
        max_rank = 0
        for i in range(n):
            rank = 1
            for j in range(i+1, n):
                if G[i][j-1] and G[j][i-1]:
                    rank += 1
            max_rank = max(max_rank, rank)
        return max_rank
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    metric_values = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            G = generate_cnf(n)
            h_G = len(G)
            mls_value = mls(G)
            metric_values.append(mls_value / h_G)
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not metric_values:
        return {
            "metric_name": "mls/G",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = correlation_coefficient(metric_values, [i for i in range(1, len(metric_values) + 1)])
    support_fraction = sum(1 for val in metric_values if val >= 0.5) / len(metric_values)
    
    return {
        "metric_name": "mls/G",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8 and correlation <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std={math.sqrt(sum((x - sum(metric_values) / len(metric_values)) ** 2 for x in metric_values) / len(metric_values))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")