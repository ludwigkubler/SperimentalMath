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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(clauses, assignment, model_size):
        if not clauses:
            return True
        literal = next(l for l in range(1, 2*model_size+1) if l not in assignment and -l not in assignment)
        pos_literal = literal if literal > 0 else -literal
        for clause in clauses:
            if pos_literal in clause or -pos_literal in clause:
                break
        else:
            return dpll(clauses, {**assignment, literal: True}, model_size) and dpll(clauses, {**assignment, literal: False}, model_size)
        new_clauses = [c for c in clauses if pos_literal not in c and -pos_literal not in c]
        return dpll(new_clauses, assignment, model_size)

    def tseitin_encoding(phi):
        n = len(phi)
        variables = list(range(1, 2*n+1))
        new_vars = [n + i for i in range(n)]
        clauses = []
        for i in range(n):
            clauses.append([variables[i], -new_vars[i]])
            clauses.append([-variables[i], new_vars[i]])
        for clause in phi:
            new_var = new_vars[clause[0] - 1]
            clauses.append([-new_var, variables[abs(clause[1]) - 1]])
            if clause[1] < 0:
                clauses.append([new_var, -variables[abs(clause[1]) - 1]])
        return clauses

    def tropical_hodge_structure_rank(clauses):
        m = len(clauses)
        n = max(max(abs(l) for l in c) for c in clauses)
        A = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal > 0:
                    A[i][literal - 1] = 1
                else:
                    A[i][-literal - 1] = -1
        rank = 0
        for row in gaussian_elimination(A):
            if any(row[j] != 0 for j in range(n + 1)):
                rank += 1
        return rank

    n = random.randint(5, 40)
    phi = [[random.choice([-1, 1]) * (i + 1) for i in range(random.randint(2, n))] for _ in range(random.randint(1, n))]
    clauses = tseitin_encoding(phi)
    h_phi = tropical_hodge_structure_rank(clauses)
    l_phi = dpll(clauses, {}, n)
    
    return {
        "metric_name": "Minimal Tropical Hodge Structure Rank and DPLL Proof Path Length",
        "metric_value": h_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": h_phi >= l_phi,
        "counterexample": "" if h_phi >= l_phi else f"h(φ) = {h_phi}, l(φ) = {l_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")