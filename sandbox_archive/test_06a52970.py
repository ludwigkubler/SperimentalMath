# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(1, n), -random.randint(1, n)]
        if random.choice([True, False]):
            clause = [-x for x in clause]
        clauses.append(clause)
    return clauses

def construct_symmetric_matrix(cnf):
    n = max(abs(lit) for clause in cnf for lit in clause)
    matrix = [[0] * n for _ in range(n)]
    for clause in cnf:
        for i, lit1 in enumerate(clause):
            for j, lit2 in enumerate(clause):
                if abs(lit1) == abs(lit2):
                    matrix[abs(lit1)-1][abs(lit2)-1] += 1
    return matrix

def gaussian_elimination(matrix):
    n = len(matrix)
    augmented_matrix = [row[:] + [0] for row in matrix]
    for i in range(n):
        if matrix[i][i] == 0:
            return None, None
        pivot = matrix[i][i]
        for j in range(i, n):
            augmented_matrix[i][j] /= pivot
        for k in range(n):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i] / pivot
                for j in range(i, n):
                    augmented_matrix[k][j] -= factor * augmented_matrix[i][j]
    return augmented_matrix, None

def min_index_of_algebraic_quotients(matrix):
    _, remainder = gaussian_elimination(matrix)
    if remainder is None:
        return None
    rank = sum(1 for row in remainder if any(x != 0 for x in row))
    return n - rank

def dpll_proof_depth(cnf, max_depth=50):
    def dpll(clause_set, assignment, depth=0):
        if not clause_set:
            return True
        if depth > max_depth:
            return False
        literals = set(lit for clause in clause_set for lit in clause)
        unit_clauses = [lit for lit in literals if any(lit == x or -lit == x for x in clause_set)]
        if unit_clauses:
            literal = unit_clauses[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clause_set if literal not in c and -literal not in c], new_assignment, depth + 1):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clause_set if literal not in c and -literal not in c], new_assignment, depth + 1):
                return True
        pure_literals = [lit for lit in literals if all(lit == x or -lit == x for x in clause_set)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clause_set if literal not in c and -literal not in c], new_assignment, depth + 1):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clause_set if literal not in c and -literal not in c], new_assignment, depth + 1):
                return True
        return False

    assignment = {}
    return dpll(cnf, assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    log_min_indices = []
    proof_depths = []

    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(int(0.1 * n**2), int(0.5 * n**2)))
            matrix = construct_symmetric_matrix(cnf)
            min_index = min_index_of_algebraic_quotients(matrix)
            if min_index is not None:
                log_min_indices.append(math.log(min_index))
                proof_depths.append(dpll_proof_depth(cnf))

    if len(log_min_indices) < 30 or len(proof_depths) < 30:
        return {
            "metric_name": "log_min_index",
            "metric_value": None,
            "instances_tested": len(log_min_indices),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }

    correlation_coefficient = sum((x - mean_log_min) * (y - mean_depth) for x, y in zip(log_min_indices, proof_depths)) / \
                              math.sqrt(sum((x - mean_log_min) ** 2 for x in log_min_indices) *
                                        sum((y - mean_depth) ** 2 for y in proof_depths))
    mean_log_min = sum(log_min_indices) / len(log_min_indices)
    mean_depth = sum(proof_depths) / len(proof_depths)

    return {
        "metric_name": "log_min_index",
        "metric_value": mean_log_min,
        "instances_tested": 30,
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / \
                  sum(1 for result in results if result["metric_value"] is not None)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None)) / \
                   sum(1 for result in results if result["metric_value"] is not None)
    support_fraction = sum(result["conjecture_holds"] for result in results if result["metric_value"] is not None) / \
                      sum(1 for result in results if result["metric_value"] is not None)

    if all(result["conjecture_holds"] for result in results if result["metric_value"] is not None):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results if result["metric_value"] is not None):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data")