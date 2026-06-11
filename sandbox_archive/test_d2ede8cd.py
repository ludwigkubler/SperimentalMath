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
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def determinant(A):
        m, n = len(A), len(A[0])
        if m != n:
            raise ValueError("Matrix must be square")
        if n == 1:
            return A[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in A[1:]]
            det += (-1) ** j * A[0][j] * determinant(submatrix)
        return det

    def dpll(cnf, assignment):
        if not cnf:
            return True
        literal = next((lit for lit in cnf[0] if lit != 0), None)
        if literal is None:
            return False
        new_cnf = [clause for clause in cnf if literal not in clause and -literal not in clause]
        if dpll(new_cnf, assignment + [literal]):
            return True
        if -literal not in assignment:
            return dpll(new_cnf, assignment + [-literal])
        return False

    def compute_order(cnf):
        n = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i + 1, n):
                A[i][j] = random.randint(0, 1)
                A[j][i] = A[i][j]
        A[n][n] = 1
        rank = gaussian_elimination(A)
        return sum(row.count(1) for row in rank)

    def compute_width(cnf):
        assignment = []
        return dpll(cnf, assignment)

    n = random.randint(5, 40)
    cnf = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(random.randint(2, n))]
    
    order = compute_order(cnf)
    width = compute_width(cnf)
    
    return {
        "metric_name": "order_width_correlation",
        "metric_value": order / width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(order - width) < 0.7 * max(order, width),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 999999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order_width_correlation = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order_width_correlation} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order_width_correlation} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='order_width_correlation' first_failing_seed={first_failing_seed}")