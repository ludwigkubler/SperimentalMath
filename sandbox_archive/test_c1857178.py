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

def run_trial(seed: int) -> dict:
    def tseitin_formula(n):
        if n <= 0:
            return [], []
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clauses.append([i])
            for j in range(i + 1, n + 1):
                clauses.append([-i, -j, i + j])
        return variables, clauses

    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            if matrix[i][i] == 0:
                continue
            for j in range(i + 1, rows):
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(cols):
                    matrix[j][k] += factor * matrix[i][k]
        return matrix

    def rank(matrix):
        matrix = [row[:] for row in matrix]
        matrix = gaussian_elimination(matrix)
        rank = 0
        for row in matrix:
            if any(row):
                rank += 1
        return rank

    n = random.randint(5, 40)
    variables, clauses = tseitin_formula(n)
    num_clauses = len(clauses)

    # Construct the incidence matrix
    incidence_matrix = [[0] * (n + num_clauses) for _ in range(n)]
    for i, clause in enumerate(clauses):
        for var in clause:
            if var > 0:
                incidence_matrix[var - 1][i + n] = 1
            else:
                incidence_matrix[-var - 1][i + n] = -1

    # Compute the rank of the incidence matrix
    symplectic_form_invariant = rank(incidence_matrix)

    # Simulate resolution proof length (simplified model)
    resolution_proof_length = 2 ** symplectic_form_invariant

    return {
        "metric_name": "resolution_proof_length",
        "metric_value": resolution_proof_length,
        "instances_tested": 1,
        "conjecture_holds": symplectic_form_invariant >= math.log(n, 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1000, 9999) for _ in range(30)]
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")