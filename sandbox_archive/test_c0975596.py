# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import itertools

def generate_cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) * (-1 if random.randint(0, 1) else 1)
                   for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for i in range(cols):
        pivot_row = -1
        for j in range(rank, rows):
            if matrix[j][i] != 0:
                pivot_row = j
                break
        if pivot_row == -1:
            continue
        matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
        for j in range(rows):
            if j != rank and matrix[j][i] != 0:
                factor = Fraction(matrix[j][i], matrix[rank][i])
                for k in range(cols):
                    matrix[j][k] -= factor * matrix[rank][k]
        rank += 1
    return rank

def hodge_representation_degree(clauses):
    n = len(clauses)
    m = len(clauses[0]) if clauses else 0
    A = [[Fraction(1, i) if i == j + 1 else Fraction(0, 1) for j in range(n)] for i in range(m)]
    rank = gaussian_elimination(A)
    return rank

def is_satisfiable(clauses):
    variables = set()
    for clause in clauses:
        variables.update(abs(var) for var in clause)
    assignment = {var: random.choice([True, False]) for var in variables}
    for clause in clauses:
        if not any(assignment[var] == (val > 0) for var, val in zip(clause, clause)):
            return False
    return True

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(1, 40)
    phi = generate_cnf(n, m)
    h_phi = hodge_representation_degree(phi)
    satisfiable = is_satisfiable(phi)
    return {
        "metric_name": "h_phi",
        "metric_value": h_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": h_phi <= m ** (Fraction(1, 3)) and satisfiable,
        "counterexample": "" if satisfiable else f"Clause count: {m}, Hodge degree: {h_phi}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_h_phi = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_h_phi) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_h_phi} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Clause count exceeds Hodge degree\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")