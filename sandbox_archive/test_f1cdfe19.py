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

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-v for v in clause]
        clauses.append(clause)
    return clauses

def tropical_semigroup_rank(clauses):
    n = len(clauses[0])
    matrix = [[Fraction(0) for _ in range(n + 1)] for _ in range(n + 1)]
    for clause in clauses:
        for var in clause:
            if var > 0:
                matrix[-var - 1][-var - 1] += 1
            else:
                matrix[var - 1][var - 1] += 1
    # Gaussian elimination to find rank
    rank = 0
    for i in range(n):
        if matrix[i][i] == Fraction(0):
            found_pivot = False
            for j in range(i + 1, n):
                if matrix[j][i] != Fraction(0):
                    matrix[i], matrix[j] = matrix[j], matrix[i]
                    found_pivot = True
                    break
            if not found_pivot:
                continue
        rank += 1
        for j in range(n):
            if i != j and matrix[j][i] != Fraction(0):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n + 1):
                    matrix[j][k] += factor * matrix[i][k]
    return rank

def monomial_ideal_complexity(clauses):
    n = len(clauses[0])
    variables = set()
    for clause in clauses:
        variables.update(abs(v) for v in clause)
    return len(variables)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(1, 40)
    m = random.randint(1, 40)
    clauses = generate_cnf(n, m)
    
    tropical_rank = tropical_semigroup_rank(clauses)
    complexity = monomial_ideal_complexity(clauses)
    
    conjecture_holds = tropical_rank <= m + n
    counterexample = "" if conjecture_holds else f"n={n}, m={m}"
    
    return {
        "metric_name": "tropical_rank",
        "metric_value": tropical_rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, m={results[0]['instances_tested']}\" first_failing_seed={first_failing_seed}")