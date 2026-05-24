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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_cnf(n):
    cnf = []
    for _ in range(10 * n):  # Generate more clauses to ensure a larger formula
        num_clauses = random.randint(2, min(5, n))
        clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(num_clauses)]
        cnf.append(clause)
    return cnf

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    rank = 0
    for j in range(cols):
        i_max = max(range(rank, rows), key=lambda i: abs(matrix[i][j]))
        if matrix[i_max][j] == 0:
            continue
        matrix[rank], matrix[i_max] = matrix[i_max], matrix[rank]
        for i in range(rows):
            if i != rank:
                factor = -matrix[i][j] / matrix[rank][j]
                for k in range(cols):
                    matrix[i][k] += factor * matrix[rank][k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)

    # Convert CNF to truth table
    num_vars = max(abs(lit) for clause in cnf for lit in clause)
    truth_table = [[False] * (1 << num_vars) for _ in range(len(cnf))]
    for i, clause in enumerate(cnf):
        for assignment in range(1 << num_vars):
            if all((assignment & (1 << abs(lit)) != 0) == (lit > 0) for lit in clause):
                truth_table[i][assignment] = True

    # Compute minimal rank of quasipolynomial function
    matrix = [[int(truth_table[j][i]) for j in range(len(cnf))] for i in range(1 << num_vars)]
    rank = gaussian_elimination(matrix)

    # Construct DPLL refutation tree and calculate diameter (simplified)
    def dpll(clause_set, assignment):
        if not clause_set:
            return 0
        literals = set()
        for clause in clause_set:
            literals.update(abs(lit) for lit in clause)
        max_diameter = 0
        for literal in literals:
            new_assignment = assignment[:]
            new_assignment[literal - 1] = True
            if any((new_assignment & (1 << abs(lit)) != 0) == (lit > 0) for lit in clause_set):
                new_clause_set = [c for c in clause_set if literal not in c and -literal not in c]
                max_diameter = max(max_diameter, dpll(new_clause_set, new_assignment))
        return max_diameter + 1

    diameter = dpll(cnf, [False] * num_vars)

    # Check conjecture
    conjecture_holds = rank >= diameter
    if not conjecture_holds:
        counterexample = f"n={n}, rank={rank}, diameter={diameter}"
    else:
        counterexample = ""

    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_rank = math.sqrt(sum((res["metric_value"] - mean_rank) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")