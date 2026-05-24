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

from fractions import Fraction
import random
import math

def generate_k_cnf(n, q):
    clauses = []
    for _ in range(q):
        clause = set()
        while len(clause) < 2:
            literal = random.randint(1, n)
            if literal not in clause and -literal not in clause:
                clause.add(literal)
        clauses.append(clause)
    return clauses

def construct_matrix(clauses, q):
    n = len(clauses[0])
    matrix = [[Fraction(0) for _ in range(n + 1)] for _ in range(q)]
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal > 0:
                matrix[i][literal] += Fraction(1)
            else:
                matrix[i][-literal] -= Fraction(1)
    return matrix

def min_rank(matrix):
    m = len(matrix)
    n = len(matrix[0])
    rank = 0
    for i in range(m):
        if all(matrix[j][i] == 0 for j in range(i, m)):
            continue
        pivot_row = i
        while matrix[pivot_row][i] == 0:
            pivot_row += 1
            if pivot_row == m:
                return rank
        matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
        for j in range(m):
            if i != j and matrix[j][i] != 0:
                factor = -matrix[j][i] / matrix[i][i]
                for k in range(n + 1):
                    matrix[j][k] += factor * matrix[i][k]
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    q = random.randint(1, min(n, 20))
    clauses = generate_k_cnf(q, n)
    matrix = construct_matrix(clauses, q)
    rank = min_rank(matrix)
    p_f = len(clauses) / q
    d_F = q / n
    c = 0.5  # Hypothetical constant for the sake of testing
    expected_rank = c * q**(1/3) * d_F**(-2/3)
    conjecture_holds = rank >= expected_rank
    counterexample = "" if conjecture_holds else f"rank={rank}, expected={expected_rank}"
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": q,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")