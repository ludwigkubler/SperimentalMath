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
            max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            for j in range(n):
                if j != i:
                    factor = Fraction(A[j][i], A[i][i])
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C
    
    def det(A):
        n = len(A)
        if n == 1:
            return A[0][0]
        elif n == 2:
            return A[0][0] * A[1][1] - A[0][1] * A[1][0]
        else:
            det_val = Fraction(0)
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in A[1:]]
                det_val += (-1) ** j * A[0][j] * det(submatrix)
            return det_val
    
    def tseitin_transform(phi, variables):
        literals = set()
        clauses = []
        for clause in phi:
            literals.update(clause)
            new_var = f"v{len(variables)}"
            variables.append(new_var)
            clauses.append([new_var])
            for literal in clause:
                if literal.startswith("~"):
                    clauses[-1].append(f"{literal[1:]}")
                else:
                    clauses[-1].append(f"~{literal}")
        return clauses, variables
    
    def hodge_zagier_rank(clauses):
        n = len(variables)
        A = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for clause in clauses:
            for literal in clause:
                if literal.startswith("~"):
                    var_index = variables.index(literal[1:])
                    A[var_index][var_index] += Fraction(1)
                else:
                    var_index = variables.index(literal)
                    A[var_index][var_index] -= Fraction(1)
        rank = 0
        for row in gaussian_elimination(A):
            if any(row[i] != Fraction(0) for i in range(n)):
                rank += 1
        return rank
    
    def resolution_width(phi, variables):
        clauses = phi[:]
        while True:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(literal in clauses[i] and f"~{literal}" in clauses[j] for literal in variables):
                        new_clause = [l for l in clauses[i] if l not in variables]
                        new_clause.extend([l for l in clauses[j] if l not in variables])
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(variables)
            clauses.append(new_clause)
    
    n = random.randint(5, 40)
    phi = [[f"v{i}", f"~v{j}"] for i in range(n) for j in range(i + 1, n)]
    clauses, variables = tseitin_transform(phi, [])
    h_z_rank = hodge_zagier_rank(clauses)
    width = resolution_width(phi, variables)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": width <= n ** (2/3),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"width > n^(2/3)\" first_failing_seed={first_failing_seed}")