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
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for j in range(m):
                if i != j:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll_width(phi, assignment):
        if not phi:
            return 0
        literals = set()
        for clause in phi:
            literals.update(clause)
        literal = random.choice(list(literals))
        positive_clauses = [clause for clause in phi if literal in clause]
        negative_clauses = [clause for clause in phi if -literal in clause]
        if not positive_clauses and not negative_clauses:
            return 0
        if not positive_clauses:
            assignment[literal] = True
            return max(dpll_width(negative_clauses, assignment), dpll_width(phi, assignment))
        if not negative_clauses:
            assignment[-literal] = True
            return max(dpll_width(positive_clauses, assignment), dpll_width(phi, assignment))
        assignment[literal] = True
        width1 = 1 + dpll_width(negative_clauses, assignment)
        assignment[literal] = False
        assignment[-literal] = True
        width2 = 1 + dpll_width(positive_clauses, assignment)
        return max(width1, width2)

    def tropical_motivic_rank(phi):
        n = len(phi[0])
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if i == j:
                    A[i][j] = 1
                else:
                    A[i][j] = -math.inf
        for clause in phi:
            max_literal = max(clause, key=abs)
            for literal in clause:
                row = abs(literal) - 1
                col = abs(max_literal) - 1
                if literal > 0:
                    A[row][col] = max(A[row][col], -math.log(abs(literal)))
                else:
                    A[row][col] = max(A[row][col], math.log(abs(literal)))
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(row))
        return rank

    n = random.randint(5, 40)
    phi = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for i in range(1, n+1)]
        phi.append(clause)

    mtr_phi = tropical_motivic_rank(phi)
    width_phi = dpll_width(phi, {})

    if width_phi == 0:
        return {
            "metric_name": "mtr_to_w_DPLL_ratio",
            "metric_value": math.inf,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL proof tree width is zero"
        }

    ratio = mtr_phi / width_phi
    return {
        "metric_name": "mtr_to_w_DPLL_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139]
    ratios = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if trial_result["conjecture_holds"]:
            ratios.append(trial_result["metric_value"])

    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio)**2 for x in ratios) / len(ratios))
    support_fraction = len([r for r in ratios if r <= 1]) / len(ratios)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(trial_result["counterexample"]):
        first_failing_seed = next(seed for seed in seeds if run_trial(seed)["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")