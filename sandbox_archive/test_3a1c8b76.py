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
        cnf = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, 4))]
            cnf.append(clause)
        return cnf
    
    def quadratic_form(cnf):
        n = len(cnf[0])
        qf = [[0] * n for _ in range(n)]
        for clause in cnf:
            for x in clause:
                if x > 0:
                    i = x - 1
                    qf[i][i] += 2
                else:
                    j = -x - 1
                    qf[j][j] -= 2
        return qf
    
    def min_integral_points(qf):
        n = len(qf)
        count = 0
        for i in range(2**n):
            point = [i >> j & 1 for j in range(n)]
            if all(point[i-1] * qf[i][j] + point[j-1] * qf[j][i] >= -qf[i][j] for i in range(1, n+1) for j in range(i)):
                count += 1
        return count
    
    def sat_entropy(cnf):
        total = sum(len(clause) for clause in cnf)
        entropy = 0
        for clause in cnf:
            p = len(clause) / total
            entropy -= p * math.log2(p)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        qf = quadratic_form(cnf)
        min_points = min_integral_points(qf)
        entropy = sat_entropy(cnf)
        results.append((min_points, entropy))
    
    if len(results) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    min_points = [r[0] for r in results]
    entropies = [r[1] for r in results]
    correlation_coefficient = sum((min_points[i] - mean_min) * (entropies[i] - mean_entropy) for i in range(len(results))) / len(results)
    mean_min = sum(min_points) / len(min_points)
    mean_entropy = sum(entropies) / len(entropies)
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical signal")