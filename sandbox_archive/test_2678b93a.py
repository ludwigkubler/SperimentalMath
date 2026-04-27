# auto-injected by SEC sandbox
import itertools
import collections
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
import json

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(i+1, n):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def asdim(X, d, max_k=32):
    n = len(X)
    best_R = float('inf')
    for k in range(1, max_k+1):
        colors = [random.randint(0, k-1) for _ in X]
        R = float('inf')
        for color in set(colors):
            pieces = []
            for x in X:
                if colors[x] == color:
                    piece = []
                    for y in X:
                        if d(x, y) <= R:
                            piece.append(y)
                    pieces.append(piece)
            min_R = float('inf')
            for piece in pieces:
                min_R = min(min_R, max(d(x, y) for x, y in itertools.combinations(piece, 2)))
            R = min(R, min_R)
        if R < best_R:
            best_R = R
    return n - math.ceil(math.log(best_R + 1))

def d_f(f, x, y):
    s = 0
    for i in range(len(x)):
        if f(x[:i] + (x[i]^y[i],) + x[i+1:]) != f(y[:i] + (x[i]^y[i],) + y[i+1:]):
            s += 1
    return math.ceil(math.log2(s))

def coarse_product(X_f, d_f, X_g, d_g):
    n = len(X_f)
    m = len(X_g)
    X_fg = [i*m + j for i in range(n) for j in range(m)]
    d_fg = [[0]*len(X_fg) for _ in range(len(X_fg))]
    for i in range(n):
        for j in range(m):
            for k in range(n):
                for l in range(m):
                    x = X_f[i]
                    y = X_g[j]
                    u = X_f[k]
                    v = X_g[l]
                    d_fg[i*m + j][k*m + l] = max(d_f(x, u), d_g(y, v))
    return X_fg, d_fg

def run_trial(seed: int) -> dict:
    random.seed(seed)
    functions = ["AND_2", "OR_2", "XOR_2", "MAJ_3", "MUX_3", "AND_3"]
    n_values = [5, 8, 11, 14]
    results = []
    
    for f_name in functions:
        for g_name in functions:
            for n in n_values:
                X_f = set()
                if f_name == "AND_2":
                    X_f = {(i, j) for i in range(2**n) for j in range(2**n) if (i & j) == 0}
                elif f_name == "OR_2":
                    X_f = {(i, j) for i in range(2**n) for j in range(2**n) if (i | j) != 0}
                elif f_name == "XOR_2":
                    X_f = {(i, j) for i in range(2**n) for j in range(2**n) if (i ^ j) != 0}
                elif f_name == "MAJ_3":
                    X_f = {(i, j, k) for i in range(2**n) for j in range(2**n) for k in range(2**n) if sum([i >> j & 1, j >> k & 1, k >> l & 1]) >= n//2 + 1}
                elif f_name == "MUX_3":
                    X_f = {(i, j, k) for i in range(2**n) for j in range(2**n) for k in range(2**n) if (i >> j & 1) ^ (k >> l & 1) == 0}
                elif f_name == "AND_3":
                    X_f = {(i, j, k) for i in range(2**n) for j in range(2**n) for k in range(2**n) if (i & j & k) != 0}
                
                d_f_val = max(d_f(f, x, y) for x, y in itertools.combinations(X_f, 2))
                asdim_X_f = asdim(X_f, d_f)
                
                X_g = set()
                if g_name == "AND_2":
                    X_g = {(i, j) for i in range(2**n) for j in range(2**n) if (i & j) == 0}
                elif g_name == "OR_2":
                    X_g = {(i, j) for i in range(2**n) for j in range(2**n) if (i | j) != 0}
                elif g_name == "XOR_2":
                    X_g = {(i, j) for i in range(2**n) for j in range(2**n) if (i ^ j) != 0}
                elif g_name == "MAJ_3":
                    X_g = {(i, j, k) for i in range(2**n) for j in range(2**n) for k in range(2**n) if sum([i >> j & 1, j >> k & 1, k >> l & 1]) >= n//2 + 1}
                elif g_name == "MUX_3":
                    X_g = {(i, j, k) for i in range(2**n) for j in range(2**n) for k in range(2**n) if (i >> j & 1) ^ (k >> l & 1) == 0}
                elif g_name == "AND_3":
                    X_g = {(i, j, k) for i in range(2**n) for j in range(2**n) for k in range(2**n) if (i & j & k) != 0}
                
                d_g_val = max(d_f(g, x, y) for x, y in itertools.combinations(X_g, 2))
                asdim_X_g = asdim(X_g, d_g)
                
                X_fg, d_fg = coarse_product(X_f, d_f, X_g, d_g)
                asdim_X_fg = asdim(X_fg, d_fg)
                
                slack = asdim_X_fg - asdim_X_f - asdim_X_g
                results.append((f_name, g_name, n, slack))
    
    total_slack = sum(slack for _, _, _, slack in results)
    min_slack = min(slack for _, _, _, slack in results)
    support_fraction = sum(1 for _, _, _, slack in results if slack >= -2) / len(results)
    and_and_support = any(slack == 0 for f, g, n, slack in results if (f, g) == ("AND_2", "AND_2"))
    xor_xor_support = any(slack == 0 for f, g, n, slack in results if (f, g) == ("XOR_2", "XOR_2"))
    
    conjecture_holds = support_fraction >= 0.95 and min_slack >= -2 and and_and_support and xor_xor_support
    counterexample = "" if conjecture_holds else f"AND_AND: {and_and_support}, XOR_XOR: {xor_xor_support}"
    
    return {
        "metric_name": "slack",
        "metric_value": total_slack / len(results),
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    total_slack = sum(result["metric_value"] * result["instances_tested"] for result in results) / len(results)
    min_slack = min(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={total_slack} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"AND_AND: {and_and_support}, XOR_XOR: {xor_xor_support}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")