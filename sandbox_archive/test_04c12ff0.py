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
    random.seed(seed)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                return None
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return [row[:n-1] for row in A]

    def dpll(clauses, assignment, literals):
        if not clauses:
            return True
        literal = literals[0]
        positive_clauses = []
        negative_clauses = []
        for clause in clauses:
            if literal in clause:
                positive_clauses.append([l for l in clause if l != literal])
            elif -literal in clause:
                negative_clauses.append([l for l in clause if l != -literal])
        if dpll(positive_clauses, assignment + [literal], literals[1:]):
            return True
        if dpll(negative_clauses, assignment + [-literal], literals[1:]):
            return True
        return False

    def hodge_index(clause):
        n = len(clause)
        A = [[0] * (n+1) for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                if clause[i] == -clause[j]:
                    A[i][j] = 1
                    A[j][i] = 1
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank

    def dpll_path_length(clauses, literals):
        assignment = []
        stack = [(clauses, assignment, literals)]
        path_length = 0
        while stack:
            clauses, assignment, literals = stack.pop()
            if not clauses:
                return path_length
            literal = literals[0]
            positive_clauses = []
            negative_clauses = []
            for clause in clauses:
                if literal in clause:
                    positive_clauses.append([l for l in clause if l != literal])
                elif -literal in clause:
                    negative_clauses.append([l for l in clause if l != -literal])
            stack.append((negative_clauses, assignment + [-literal], literals[1:]))
            path_length += 1
            stack.append((positive_clauses, assignment + [literal], literals[1:]))
            path_length += 1
        return path_length

    n = random.randint(5, 40)
    clauses = []
    for _ in range(n):
        clause = random.sample(range(-n, -1), random.randint(1, n))
        clauses.append(clause)

    hodge_values = [hodge_index(clause) for clause in clauses]
    dpll_lengths = [dpll_path_length(clauses, list(range(1, n+1))) for _ in range(30)]

    if not all(hodge_values):
        return {
            "metric_name": "Hodge Index",
            "metric_value": sum(hodge_values) / len(hodge_values),
            "instances_tested": len(hodge_values),
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    correlation = 0
    for i in range(len(hodge_values)):
        h1, d1 = hodge_values[i], dpll_lengths[i]
        for j in range(i+1, len(hodge_values)):
            h2, d2 = hodge_values[j], dpll_lengths[j]
            correlation += (h1 - h2) * (d1 - d2)
    correlation /= len(hodge_values) * len(hodge_values)

    return {
        "metric_name": "Hodge Index",
        "metric_value": correlation,
        "instances_tested": len(hodge_values),
        "n_max": n,
        "conjecture_holds": abs(correlation) >= 0.7 and max(abs(h - d) for h, d in zip(hodge_values, dpll_lengths)) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")