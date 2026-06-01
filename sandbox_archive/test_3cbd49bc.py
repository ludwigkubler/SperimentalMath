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
            max_row = i + max(range(i, m), key=lambda j: abs(A[j][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A
    
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
    
    def frege_proof_depth(phi):
        stack = []
        depth = 0
        max_depth = 0
        for token in phi:
            if token == '(': 
                stack.append(token)
                depth += 1
                max_depth = max(max_depth, depth)
            elif token == ')':
                stack.pop()
                depth -= 1
        return max_depth
    
    def tropicalize(phi):
        n = len(phi[0])
        T = [[math.inf] * n for _ in range(n)]
        for i in range(n):
            T[i][i] = 0
        for clause in phi:
            for literal in clause:
                if literal.startswith('¬'):
                    var = int(literal[1:]) - 1
                    T[var][var] = min(T[var][var], 1)
                else:
                    var = int(literal) - 1
                    T[var][var] = min(T[var][var], 0)
        return T
    
    def minimal_local_ring_unit_group_size(T):
        n = len(T)
        I = [[int(i == j) for j in range(n)] for i in range(n)]
        A = [row[:] + col[:] for row, col in zip(T, I)]
        A = gaussian_elimination(A)
        rank = sum(1 for row in A if any(x != 0 for x in row))
        return n - rank
    
    def generate_k_cnf(k, n):
        phi = []
        for _ in range(n):
            clause = random.sample(range(1, n+1), k)
            phi.append([f"{x}" if random.choice([True, False]) else f"¬{x}" for x in clause])
        return phi
    
    def correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        var_x = sum((x[i] - mean_x) ** 2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y) ** 2 for i in range(n)) / n
        return cov / (math.sqrt(var_x) * math.sqrt(var_y))
    
    def p_value(r, n):
        t = r * math.sqrt((n - 2) / (1 - r**2))
        df = n - 2
        if abs(t) > 1.96:
            return 0.05
        else:
            return 1.0
    
    k = random.randint(2, 3)
    n = random.randint(5, 40)
    phi = generate_k_cnf(k, n)
    
    T = tropicalize(phi)
    mu_phi = minimal_local_ring_unit_group_size(T)
    d_phi = frege_proof_depth(phi)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient([mu_phi], [d_phi]),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if d_phi == 0 else True,
        "counterexample": "" if d_phi != 0 else "Frege proof depth is zero"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")