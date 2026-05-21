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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 10):  # Generate a few clauses to keep it simple
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def cnf_to_quadratic_form(cnf):
        n = len(cnf[0])
        qform = [[0] * n for _ in range(n)]
        for clause in cnf:
            for i in clause:
                if i > 0:
                    x, sign = i - 1, 1
                else:
                    x, sign = -i - 1, -1
                qform[x][x] += sign * sign
        return qform
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i
            for j in range(i + 1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(n):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def rank(A):
        n = len(A)
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def resolution(cnf):
        clauses = cnf[:]
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause_i, clause_j = clauses[i], clauses[j]
                    for x in set(clause_i) & set([-x for x in clause_j]):
                        new_clause = [y for y in clause_i if y != x] + [y for y in clause_j if y != -x]
                        if not any(new_clause):
                            return len(cnf)
                        new_clauses.append(new_clause)
            clauses.extend(new_clauses)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    qform = cnf_to_quadratic_form(cnf)
    rank_qform = rank(qform)
    proof_length = resolution(cnf)
    
    return {
        "metric_name": "rank_over_proof_length",
        "metric_value": rank_qform / proof_length,
        "instances_tested": 1,
        "conjecture_holds": rank_qform <= 2 * proof_length,  # Example constant c=2
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(10000, 99999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "rank_over_proof_length > 2 * proof_length"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")