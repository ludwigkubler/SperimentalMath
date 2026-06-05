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
    
    def generate_formula(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(clause[i] == 0 for i in range(n)):
                continue
            clauses.append(clause)
        return clauses
    
    def projective_volume(clauses):
        n = len(clauses[0])
        points = set()
        for clause in clauses:
            point = [0] * n
            for literal, var in enumerate(clause):
                if literal > 0:
                    point[var - 1] += 1
                else:
                    point[-var - 1] -= 1
            points.add(tuple(point))
        return len(points)
    
    def communication_complexity_rank(clauses):
        n = len(clauses[0])
        rank = 0
        for i in range(n):
            active_clauses = [c for c in clauses if c[i] != 0]
            if active_clauses:
                rank += 1
        return rank
    
    def correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((x_i - mean_x) * (y_i - mean_y) for x_i, y_i in zip(x, y)) / len(x)
        var_x = sum((x_i - mean_x) ** 2 for x_i in x) / len(x)
        var_y = sum((y_i - mean_y) ** 2 for y_i in y) / len(y)
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    sv_values = []
    ccrank_values = []
    
    for n in n_values:
        formula = generate_formula(n)
        sv = projective_volume(formula)
        ccrank = communication_complexity_rank(formula)
        sv_values.append(sv)
        ccrank_values.append(ccrank)
    
    corr = correlation(sv_values, ccrank_values)
    
    return {
        "metric_name": "Correlation",
        "metric_value": corr,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": corr >= 0.5 and all(corr >= 0.3 for _ in range(30)),
        "counterexample": "" if corr >= 0.5 else f"Correlation {corr} < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation < 0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")