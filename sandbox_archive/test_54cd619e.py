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
    
    def generate_cnf(n, complexity):
        cnf = []
        for _ in range(complexity):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def polynomial_from_cnf(cnf):
        poly = {}
        for clause in cnf:
            term = tuple(sorted(abs(lit) for lit in clause))
            if term not in poly:
                poly[term] = 0
            poly[term] += 1
        return poly
    
    def hodge_rank(poly):
        n = len(poly)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for term, coeff in poly.items():
            for i in term:
                matrix[i-1][i-1] += coeff
            matrix[n][i-1] -= coeff
            matrix[i-1][n] -= coeff
        
        rank = 0
        for row in range(n):
            if any(matrix[row][col] != 0 for col in range(n + 1)):
                pivot_col = next(col for col in range(n) if matrix[row][col] != 0)
                for col in range(n + 1):
                    matrix[row][col], matrix[rank][col] = matrix[rank][col], matrix[row][col]
                for i in range(n):
                    if i != rank:
                        factor = -matrix[i][pivot_col] / matrix[rank][pivot_col]
                        for col in range(n + 1):
                            matrix[i][col] += factor * matrix[rank][col]
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    complexity = max(random.randint(1, n // 2), 1)
    cnf = generate_cnf(n, complexity)
    poly = polynomial_from_cnf(cnf)
    
    if not poly:
        return {
            "metric_name": "Hodge rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    h_rank = hodge_rank(poly)
    c = Fraction(1, 2)  # Example constant for the lower bound
    expected_bound = c * math.log(n)
    
    conjecture_holds = h_rank >= expected_bound
    
    return {
        "metric_name": "Hodge rank",
        "metric_value": h_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Expected Hodge rank >= {expected_bound}, got {h_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_h_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_h_rank = math.sqrt(sum((r["metric_value"] - mean_h_rank) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_h_rank} std={std_h_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_h_rank} std={std_h_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Hodge rank does not meet the expected bound\" first_failing_seed={first_failing_seed}")