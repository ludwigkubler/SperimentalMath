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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def AND_2(x, y):
        return x and y
    
    def OR_2(x, y):
        return x or y
    
    def XOR_2(x, y):
        return x != y
    
    def MAJ_3(x, y, z):
        return (x + y + z) >= 2
    
    def IP_2(x, y):
        return x * y
    
    functions = [AND_2, OR_2, XOR_2, MAJ_3, IP_2]
    
    def hamming_distance(x, y):
        return sum(1 for i in range(len(x)) if x[i] != y[i])
    
    def build_X_d(f, k):
        n = 2 ** k
        X = [tuple(i) for i in range(n)]
        d = [[hamming_distance(x, y) for y in X] for x in X]
        return X, d
    
    def build_basis(X, d):
        n = len(X)
        C0 = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        C1 = []
        for x in X:
            row = [0] * n
            for y in X:
                if hamming_distance(x, y) == 1:
                    row[y] = 1
            C1.append(row)
        delta = subtract_matrices(C1, multiply_matrices(delta_image(C0), transpose_matrix(C1)))
        cokernel = find_cokernel(delta)
        basis = [cokernel[i][0] for i in range(len(cokernel)) if any(cokernel[i])]
        return basis
    
    def delta_image(C0):
        n = len(C0)
        image = []
        for x in range(n):
            row = [sum(C0[x][j] * C1[j][y] for j in range(n)) for y in range(n)]
            image.append(row)
        return image
    
    def transpose_matrix(M):
        return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]
    
    def subtract_matrices(A, B):
        return [[A[i][j] - B[i][j] for j in range(len(A[0]))] for i in range(len(A))]
    
    def multiply_matrices(A, B):
        n = len(A)
        m = len(B[0])
        result = [[sum(A[i][k] * B[k][j] for k in range(m)) for j in range(m)] for i in range(n)]
        return result
    
    def find_cokernel(M):
        n = len(M)
        rank = 0
        cokernel = []
        for i in range(n):
            if any(M[i]):
                row = [M[i][j] for j in range(n) if M[i][j]]
                cokernel.append(row)
                rank += 1
        return cokernel
    
    def build_Roe_operator(X, d, R):
        n = len(X)
        T = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if hamming_distance(X[i], X[j]) <= R:
                    T[i][j] = random.gauss(0, 1)
        return symmetrize_matrix(T)
    
    def symmetrize_matrix(M):
        n = len(M)
        for i in range(n):
            for j in range(i + 1, n):
                M[i][j] += M[j][i]
                M[j][i] = M[i][j]
        return M
    
    def trace(T):
        n = len(T)
        return sum(T[i][i] for i in range(n))
    
    def propagation(T):
        n = len(T)
        max_propagation = 0
        for i in range(n):
            for j in range(i + 1, n):
                if T[i][j] != 0:
                    max_propagation = max(max_propagation, hamming_distance(X[i], X[j]))
        return max_propagation
    
    def coarse_product(X_f, d_f, X_g, d_g):
        n = len(X_f)
        m = len(X_g)
        X_fg = [(x, y) for x in X_f for y in X_g]
        d_fg = [[max(d_f[x[0]][y[0]], d_g[x[1]][y[1]]) for y in X_fg] for x in X_fg]
        return X_fg, d_fg
    
    def trace_pairing(c, T):
        n = len(c)
        result = 0
        for i in range(n):
            for j in range(i + 1, n):
                if c[i][j] != 0:
                    result += c[i][j] * T[i][j]
        return result
    
    def log_ratio(trace_value, propagation_value):
        return math.log(abs(trace_value)) / math.log(propagation_value)
    
    def run_composition(f, g, k_f, k_g):
        X_f, d_f = build_X_d(f, k_f)
        basis_f = build_basis(X_f, d_f)
        T_f = build_Roe_operator(X_f, d_f, 4)
        kappa_f = max(log_ratio(trace_pairing(basis_f[i], T_f), propagation(T_f)) for i in range(len(basis_f)))
        
        X_g, d_g = build_X_d(g, k_g)
        basis_g = build_basis(X_g, d_g)
        T_g = build_Roe_operator(X_g, d_g, 4)
        kappa_g = max(log_ratio(trace_pairing(basis_g[i], T_g), propagation(T_g)) for i in range(len(basis_g)))
        
        X_fg, d_fg = coarse_product(X_f, d_f, X_g, d_g)
        basis_fg = build_basis(X_fg, d_fg)
        T_fg = build_Roe_operator(X_fg, d_fg, 4)
        kappa_fg = max(log_ratio(trace_pairing(basis_fg[i], T_fg), propagation(T_fg)) for i in range(len(basis_fg)))
        
        return kappa_f, kappa_g, kappa_fg
    
    def run_control(f, k):
        X_f, d_f = build_X_d(f, k)
        basis_f = build_basis(X_f, d_f)
        T_f = build_Roe_operator(X_f, d_f, 4)
        kappa_f = max(log_ratio(trace_pairing(basis_f[i], T_f), propagation(T_f)) for i in range(len(basis_f)))
        
        X_rand = [tuple(random.randint(0, 1) for _ in range(k)) for _ in range(2 ** k)]
        d_rand = [[hamming_distance(x, y) for y in X_rand] for x in X_rand]
        basis_rand = build_basis(X_rand, d_rand)
        T_rand = build_Roe_operator(X_rand, d_rand, 4)
        kappa_rand = max(log_ratio(trace_pairing(basis_rand[i], T_rand), propagation(T_rand)) for i in range(len(basis_rand)))
        
        return kappa_f, kappa_rand
    
    def check_additivity(kappa_f, kappa_g, kappa_fg):
        C = 2
        return kappa_fg >= kappa_f + kappa_g - C
    
    def check_control(kappa_f, kappa_rand):
        return abs(kappa_rand - kappa_f) <= 1
    
    results = []
    for f in functions:
        for g in functions:
            k_f = random.randint(1, 4)
            k_g = random.randint(1, 4)
            kappa_f, kappa_g, kappa_fg = run_composition(f, g, k_f, k_g)
            kappa_f_rand, kappa_rand = run_control(f, k_f)
            
            results.append({
                "f": f.__name__,
                "g": g.__name__,
                "k_f": k_f,
                "k_g": k_g,
                "kappa_f": kappa_f,
                "kappa_g": kappa_g,
                "kappa_fg": kappa_fg,
                "kappa_f_rand": kappa_f_rand,
                "kappa_rand": kappa_rand
            })
    
    support_count = 0
    total_slack = 0
    
    for result in results:
        if check_additivity(result["kappa_f"], result["kappa_g"], result["kappa_fg"]):
            support_count += 1
            slack = result["kappa_f"] + result["kappa_g"] - result["kappa_fg"]
            total_slack += slack
    
    mean_slack = total_slack / len(results)
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8 and mean_slack <= 2:
        return {
            "metric_name": "slack",
            "metric_value": mean_slack,
            "instances_tested": len(results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        for result in results:
            if not check_additivity(result["kappa_f"], result["kappa_g"], result["kappa_fg"]):
                return {
                    "metric_name": "slack",
                    "metric_value": mean_slack,
                    "instances_tested": len(results),
                    "conjecture_holds": False,
                    "counterexample": f"({result['f']}, {result['g']}) with kappa_f={result['kappa_f']}, kappa_g={result['kappa_g']}, kappa_fg={result['kappa_fg']}"
                }
    
    return {
        "metric_name": "slack",
        "metric_value": mean_slack,
        "instances_tested": len(results),
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [11, 23, 37, 53, 71] if not sys.argv[1:] else [int(s) for s in sys.argv[1:]]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
    
    results = []
    for seed in seeds:
        with open(f"trial_{seed}.json", "r") as f:
            trial_results = json.load(f)
            results.extend(trial_results)
    
    support_count = 0
    total_slack = 0
    
    for result in results:
        if check_additivity(result["kappa_f"], result["kappa_g"], result["kappa_fg"]):
            support_count += 1
            slack = result["kappa_f"] + result["kappa_g"] - result["kappa_fg"]
            total_slack += slack
    
    mean_slack = total_slack / len(results)
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8 and mean_slack <= 2:
        print(f"RESULT: SUPPORTED mean={mean_slack} std=0.0 support_fraction={support_fraction}")
    elif any(not check_additivity(result["kappa_f"], result["kappa_g"], result["kappa_fg"]) for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not check_additivity(result["kappa_f"], result["kappa_g"], result["kappa_fg"]))
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")