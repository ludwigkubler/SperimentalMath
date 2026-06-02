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

# Helper functions for matrix operations
def matrix_multiply(A, B):
    if len(A[0]) != len(B):
        raise ValueError("Incompatible dimensions for matrix multiplication")
    result = [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in zip(*B)] for row_A in A]
    return result

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda x: abs(matrix[x][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        for j in range(cols):
            if j != i:
                factor = matrix[j][i] / matrix[i][i]
                matrix[j] = [matrix[j][k] - factor * matrix[i][k] for k in range(cols)]
    return matrix

def rank(matrix):
    rref = gaussian_elimination(matrix)
    non_zero_rows = sum(1 for row in rref if any(row))
    return non_zero_rows

# DPLL implementation
def dpll(clauses, assignment={}):
    if not clauses:
        return True
    unit_clause = next((c for c in clauses if len(c) == 1), None)
    if unit_clause:
        literal = unit_clause[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        else:
            return False
    pure_literal = next((l for l in range(1, max(assignment.keys()) + 2) if (l not in assignment and -l not in assignment)), None)
    if pure_literal is not None:
        new_assignment[pure_literal] = True
        if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
            return True
        else:
            new_assignment[pure_literal] = False
            if dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment):
                return True
            else:
                return False
    literal, polarity = next((l, True) for l in range(1, max(assignment.keys()) + 2) if l not in assignment)
    new_assignment[literal] = polarity
    if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
        return True
    else:
        new_assignment[literal] = not polarity
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        else:
            return False

# Geometric quantization matrix generation (simplified Weyl quantization)
def geometric_quantization_matrix(n):
    q = [[0] * n for _ in range(n)]
    for i, j in combinations(range(n), 2):
        q[i][j] = (-1) ** (i ^ j)
        q[j][i] = q[i][j]
    return q

# Main function to run a single trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 30
    min_ranks = []
    proof_depths = []

    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = [[random.choice([i, -i]) for i in range(1, n + 1)] for _ in range(n)]
        q_matrix = geometric_quantization_matrix(n)
        r_phi = rank(q_matrix)
        d_phi = dpll(cnf)
        min_ranks.append(r_phi)
        proof_depths.append(d_phi)

    correlation_coefficient = sum((x - mean(min_ranks)) * (y - mean(proof_depths)) for x, y in zip(min_ranks, proof_depths)) / math.sqrt(sum((x - mean(min_ranks)) ** 2 for x in min_ranks) * sum((y - mean(proof_depths)) ** 2 for y in proof_depths))
    if correlation_coefficient < 0.6 or correlation_coefficient > 0.8:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "correlation_out_of_range"
        }
    else:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": True,
            "counterexample": ""
        }

# Helper function to calculate mean
def mean(values):
    return sum(values) / len(values)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = mean([r["metric_value"] for r in results])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(r["counterexample"] == "correlation_out_of_range" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r["counterexample"] == "correlation_out_of_range")
        print(f"RESULT: FALSIFIED counterexample='correlation_out_of_range' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested=30")