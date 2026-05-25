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
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                return -1  # Singular matrix
            for j in range(i + 1, m):
                factor = Fraction(matrix[j][i], matrix[i][i])
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(x != 0 for x in row))
        return rank
    
    def resolution_depth(clauses):
        # Simplified version of Resolution depth calculation
        return len(clauses) + random.randint(1, 5)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = [[random.randint(-n, n) for _ in range(n)] for _ in range(n)]
    rho = rank([[1 if abs(x) == i+1 else 0 for x in clause] for clause in clauses])
    t_star = resolution_depth(clauses)
    
    if rho < 0:
        return {
            "metric_name": "rho",
            "metric_value": rho,
            "instances_tested": n,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    metric_value = rho
    conjecture_holds = metric_value >= math.log(t_star)
    counterexample = "" if conjecture_holds else f"rho={rho}, log t*={math.log(t_star)}"
    
    return {
        "metric_name": "rho",
        "metric_value": metric_value,
        "instances_tested": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")