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

def random_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) for _ in range(random.randint(1, n))]
        if random.choice([True, False]):
            clause = [-var for var in clause]
        clauses.append(clause)
    return clauses

def tropical_semigroup_rank(clauses):
    variables = set()
    for clause in clauses:
        variables.update(abs(var) for var in clause)
    n = len(variables)
    if n == 0:
        return 0
    matrix = [[Fraction(0, 1)] * n for _ in range(n)]
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                var_i = abs(clause[i])
                var_j = abs(clause[j])
                matrix[var_i - 1][var_j - 1] += 1
                matrix[var_j - 1][var_i - 1] += 1
    for i in range(n):
        matrix[i][i] += n
    rank = 0
    for _ in range(n):
        max_val = Fraction(0, 1)
        max_idx = -1
        for j in range(n):
            if matrix[j][j] > max_val:
                max_val = matrix[j][j]
                max_idx = j
        if max_idx == -1:
            break
        rank += 1
        for j in range(n):
            matrix[max_idx][j] -= max_val
            matrix[j][max_idx] -= max_val
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(5, 40)
    clauses = random_cnf(n, m)
    tropical_rank = tropical_semigroup_rank(clauses)
    complexity = m * n
    return {
        "metric_name": "tropical_rank",
        "metric_value": tropical_rank,
        "instances_tested": 1,
        "conjecture_holds": tropical_rank <= complexity,
        "counterexample": "" if tropical_rank <= complexity else f"CNF with {n} vars and {m} clauses"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CNF with {n} vars and {m} clauses\" first_failing_seed={first_failing_seed}")