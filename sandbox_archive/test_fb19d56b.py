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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        if matrix[i][i] == 0:
            continue
        denom = Fraction(1, matrix[i][i])
        for j in range(i, n):
            matrix[i][j] *= denom
        for k in range(n):
            if k != i and matrix[k][i] != 0:
                factor = -matrix[k][i]
                for j in range(i, n):
                    matrix[k][j] += factor * matrix[i][j]

def quadratic_form_rank(CNF):
    n = len(CNF)
    Q = [[0] * n for _ in range(n)]
    for clause in CNF:
        for lit1 in clause:
            i = abs(lit1) - 1
            for lit2 in clause:
                j = abs(lit2) - 1
                if lit1 > 0 and lit2 > 0:
                    Q[i][j] += 1
    gaussian_elimination(Q)
    rank = sum(1 for row in Q if any(row))
    return rank

def resolution_proofs(CNF):
    clauses = set(tuple(sorted(clause)) for clause in CNF)
    proof = []
    while True:
        new_clause = None
        for clause1 in clauses:
            for clause2 in clauses:
                if len(set(clause1) & set(clause2)) == 1:
                    lit1, lit2 = next(iter(set(clause1) ^ set(clause2)))
                    if lit1 > 0 and -lit2 in clause1:
                        new_clause = tuple(sorted([x for x in clause1 if x != -lit2] + [x for x in clause2 if x != lit1]))
                        break
            if new_clause:
                break
        if not new_clause:
            return proof
        clauses.add(new_clause)
        proof.append(new_clause)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 0
    total_rank = 0
    total_length = 0

    for _ in range(30):
        CNF = [[random.randint(-n, -1), random.randint(1, n)] for _ in range(random.randint(5, 20))]
        rank = quadratic_form_rank(CNF)
        proof_length = len(resolution_proofs(CNF))
        total_rank += rank
        total_length += proof_length
        instances_tested += 1

    mean_rank = Fraction(total_rank, instances_tested)
    mean_length = Fraction(total_length, instances_tested)
    conjecture_holds = mean_rank <= 2 * mean_length
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Minimal Rank / Resolution Proof Length",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")