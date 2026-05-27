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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i
        for j in range(i + 1, rows):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(i, cols):
            matrix[i][j] /= pivot
        for j in range(rows):
            if j != i and matrix[j][i] != 0:
                factor = matrix[j][i]
                for k in range(i, cols):
                    matrix[j][k] -= factor * matrix[i][k]

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    augmented_matrix = [row + [1 if i == j else 0 for j in range(cols)] for i, row in enumerate(matrix)]
    gaussian_elimination(augmented_matrix)
    rank_value = sum(1 for row in augmented_matrix if any(row[j] != 0 for j in range(cols)))
    return rank_value

def generate_3cnf(n):
    clauses = []
    variables = list(range(1, n + 1))
    for _ in range(2 * n):
        clause = random.sample(variables, 3)
        clause = [random.choice([-1, 1]) * var for var in clause]
        clauses.append(clause)
    return clauses

def twisted_quantum_entanglement_tensor(clauses):
    n = len(clauses[0])
    tensor = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for i, var1 in enumerate(clause):
            for j, var2 in enumerate(clause[i + 1:], start=i + 1):
                tensor[abs(var1)][abs(var2)] += 1
                tensor[abs(var2)][abs(var1)] += 1
    return tensor

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    clauses = generate_3cnf(n)
    tensor = twisted_quantum_entanglement_tensor(clauses)
    rank_value = rank(tensor)
    metric_value = rank_value
    instances_tested = 1
    conjecture_holds = rank_value >= (1 + 1e-6) * n**(2/3)
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank_value}"
    return {
        "metric_name": "Rank of Twisted Quantum Entanglement Tensor",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={res['instances_tested']}, rank={res['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")