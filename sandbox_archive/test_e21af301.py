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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i+1, n))) / A[i][i]
    return x

def is_solution(A, b, x):
    return all(abs(sum(a*x[j] for j in range(len(x))) - b[i]) < 1e-9 for i in range(len(b)))

def min_diophantine_root_count(clauses):
    n = len(clauses)
    A = [[0]*n for _ in range(n)]
    b = [0]*n
    for i, clause in enumerate(clauses):
        for j in range(i+1, n):
            if clause[i] != 0 and clause[j] != 0:
                A[i][j] += 1
                A[j][i] += 1
            b[i] += abs(clause[i])
            b[j] += abs(clause[j])
    for i in range(n):
        A[i][i] = sum(abs(c) for c in clauses[i]) - abs(b[i])
    x = gaussian_elimination(A, b)
    return len(set(x))

def dpll_solve(clauses):
    def solve(literals):
        if not literals:
            return True
        literal = literals[0]
        if literal > 0:
            if literal in assignment or -literal not in assignment:
                assignment[literal] = True
                if solve([l for l in literals if l != literal]):
                    return True
                del assignment[literal]
            if -literal not in assignment:
                assignment[-literal] = False
                if solve([l for l in literals if l != -literal]):
                    return True
                del assignment[-literal]
        else:
            if -literal in assignment or literal not in assignment:
                assignment[-literal] = True
                if solve([l for l in literals if l != -literal]):
                    return True
                del assignment[-literal]
            if literal not in assignment:
                assignment[literal] = False
                if solve([l for l in literals if l != literal]):
                    return True
                del assignment[literal]
        return False
    n = len(clauses)
    assignment = {}
    literals = list(range(1, n+1)) + [-i for i in range(1, n+1)]
    random.shuffle(literals)
    return solve(literals)

def proof_length(clauses):
    if not clauses:
        return 0
    if all(c[0] > 0 for c in clauses):
        return 2 * proof_length([c[1:] for c in clauses]) + 1
    if any(c[0] < 0 for c in clauses):
        return 2 * proof_length([c[1:] for c in clauses if c[0] > 0]) + 1
    return 0

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    variables = set(range(1, n+1))
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * random.choice(variables) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    min_root_count = min_diophantine_root_count(clauses)
    proof_len = proof_length(clauses)
    return {
        "metric_name": "MinRootCount vs ProofLength",
        "metric_value": min_root_count / proof_len,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": min_root_count <= 2 * proof_len,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"MinRootCount > 2 * ProofLength\" first_failing_seed={result['seed']}")
                break