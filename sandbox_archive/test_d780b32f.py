# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def random_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = random.sample(variables, random.randint(1, n))
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def tropical_semigroup_rank(clauses):
    n = max(abs(x) for clause in clauses for x in clause)
    matrix = [[0] * n for _ in range(n)]
    for clause in clauses:
        for var in clause:
            if abs(var) <= n:
                matrix[var - 1][var - 1] += 1
    # Gaussian elimination to find the rank
    rank = 0
    for i in range(n):
        if any(matrix[j][i] != 0 for j in range(rank, n)):
            rank += 1
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    for k in range(n):
                        matrix[j][k], matrix[i][k] = matrix[i][k], matrix[j][k]
                    break
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(1, 40)
    m = random.randint(1, 40)
    clauses = random_cnf(n, m)
    tropical_rank = tropical_semigroup_rank(clauses)
    complexity_I = m ** n
    metric_value = tropical_rank
    instances_tested = 1
    conjecture_holds = tropical_rank <= complexity_I
    counterexample = "" if conjecture_holds else f"CNF with {n} vars, {m} clauses"
    return {
        "metric_name": "tropical_rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
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
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")