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
            for j in range(i+1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B[0]), len(B)
        C = [[0 for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if m == 1:
            return A[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def min_local_system_rank(clause_set):
        m = len(clause_set)
        n = max(abs(literal) for clause in clause_set for literal in clause if literal != 0)
        A = [[0 for _ in range(n)] for _ in range(m)]
        for i, clause in enumerate(clause_set):
            for literal in clause:
                if literal != 0:
                    A[i][abs(literal) - 1] += 1
        rank = 0
        for row in gaussian_elimination(A):
            if any(row[j] != 0 for j in range(n)):
                rank += 1
        return rank

    def clause_set_complexity(clause_set):
        literals = set()
        for clause in clause_set:
            literals.update(abs(literal) for literal in clause if literal != 0)
        return len(literals)

    n_max = 40
    instances_tested = 0
    total_r_local = Fraction(0)
    total_s_clauses = Fraction(0)

    for m in range(5, n_max + 1):
        for _ in range(6):  # 30 instances per seed (6 trials per size)
            clause_set = []
            for _ in range(m):
                literals = random.sample(range(-m, m+1), random.randint(2, min(4, m)))
                literals = [l for l in literals if l != 0]
                clause_set.append(literals)
            r_local = min_local_system_rank(clause_set)
            s_clauses = clause_set_complexity(clause_set)
            total_r_local += Fraction(r_local)
            total_s_clauses += Fraction(s_clauses)
            instances_tested += 1

    if instances_tested == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }

    mean_r_local = total_r_local / instances_tested
    mean_s_clauses = total_s_clauses / instances_tested

    covariance = Fraction(0)
    for m in range(5, n_max + 1):
        for _ in range(6):
            clause_set = []
            for _ in range(m):
                literals = random.sample(range(-m, m+1), random.randint(2, min(4, m)))
                literals = [l for l in literals if l != 0]
                clause_set.append(literals)
            r_local = min_local_system_rank(clause_set)
            s_clauses = clause_set_complexity(clause_set)
            covariance += (r_local - mean_r_local) * (s_clauses - mean_s_clauses)

    variance_r_local = Fraction(0)
    for m in range(5, n_max + 1):
        for _ in range(6):
            clause_set = []
            for _ in range(m):
                literals = random.sample(range(-m, m+1), random.randint(2, min(4, m)))
                literals = [l for l in literals if l != 0]
                clause_set.append(literals)
            r_local = min_local_system_rank(clause_set)
            variance_r_local += (r_local - mean_r_local) ** 2

    pearson_corr_coeff = covariance / math.sqrt(variance_r_local * instances_tested)

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": float(pearson_corr_coeff),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr_coeff >= 0.8,
        "counterexample": "" if pearson_corr_coeff >= 0.8 else "Pearson correlation coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")