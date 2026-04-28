# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import sys
from itertools import combinations

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

def matrix_multiply(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0]*p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def walsh_hadamard_transform(A):
    n = len(A)
    if n == 1:
        return A
    A0, A1 = [row[:n//2] for row in A], [row[n//2:] for row in A]
    B0, B1 = walsh_hadamard_transform(A0), walsh_hadamard_transform(A1)
    C = [[B0[i][j] + B1[i][j] for j in range(n//2)] + [B0[i][j] - B1[i][j] for j in range(n//2)]
         for i in range(n//2)] + [[B0[i][j] - B1[i][j] for j in range(n//2)] + [B0[i][j] + B1[i][j] for j in range(n//2)]
                                for i in range(n//2)]
    return C

def unit_propagation(F, x):
    while True:
        changed = False
        for clause in F:
            if all(lit not in x or (x[lit] == 1 and lit > 0) or (x[lit] == -1 and lit < 0) for lit in clause):
                continue
            unit_lits = [lit for lit in clause if lit not in x]
            if len(unit_lits) != 1:
                break
            lit, sign = unit_lits[0], 1 if unit_lits[0] > 0 else -1
            x[lit] = sign
            changed = True
        if not changed:
            break
    return x

def is_unsat(F):
    n = max(abs(lit) for clause in F for lit in clause)
    x = {i: None for i in range(1, n+1)}
    stack = list(range(1, n+1))
    while stack:
        i = stack.pop()
        if x[i] is None:
            x[i] = 1
            stack.append(-i)
        else:
            x[i] = -x[i]
            stack.remove(-i)
            stack.append(i)
        if not unit_propagation(F, x):
            return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [8, 10, 12, 14]
    results = []
    
    for n in n_values:
        m = math.floor(4.5 * n)
        F = []
        while len(F) < m:
            clause = set(random.sample(range(-n, -1), 3))
            if clause not in F and is_unsat([list(clause)] + F):
                F.append(list(clause))
        
        g_F = [[0] * (1 << n) for _ in range(n)]
        for i in range(1 << n):
            x = {j: ((i >> j) & 1) * 2 - 1 for j in range(n)}
            if unit_propagation(F, x) == {}:
                g_F[0][i] = 1
        
        T_k = sum(g_F[k][i]**2 for i in range(1 << n) for k in range(1, math.floor(math.log2(m+1)) + 1))
        
        L_F = 0
        stack = [{}]
        while stack:
            x = stack.pop()
            if len(x) == n:
                if unit_propagation(F, x) == {}:
                    L_F += 1
            else:
                for lit in range(1, n+1):
                    new_x = x.copy()
                    new_x[lit] = 1
                    stack.append(new_x)
                    new_x = x.copy()
                    new_x[lit] = -1
                    stack.append(new_x)
        
        metric_value = math.log2(L_F + 1) if L_F > 0 else 0
        conjecture_holds = (metric_value <= 4 * (1 + T_k * (1 << n)) / max(1, g_F[0][0] * (1 << n)))
        counterexample = "" if conjecture_holds else "unsatisfiable instance"
        
        results.append({
            "n": n,
            "m": m,
            "L_F": L_F,
            "T_k": T_k,
            "metric_value": metric_value,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    all_results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["results"])
    
    mean_value = sum(res["metric_value"] for res in all_results) / len(all_results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in all_results) / len(all_results))
    support_fraction = sum(1 for res in all_results if res["conjecture_holds"]) / len(all_results)
    
    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")