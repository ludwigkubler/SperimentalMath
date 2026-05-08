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
from scipy.optimize import linprog

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find the pivot row
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        for j in range(i+1, m):
            factor = A[j][i] / A[i][i]
            for k in range(n):
                A[j][k] -= factor * A[i][k]

    return A

def back_substitution(A, b):
    m, n = len(A), len(b)
    x = [0] * m
    for i in range(m-1, -1, -1):
        sum_val = 0
        for j in range(i+1, m):
            sum_val += A[i][j] * x[j]
        x[i] = (b[i] - sum_val) / A[i][i]
    return x

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0 for _ in range(p)] for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_ac0_circuit(depth, size):
        if depth == 1:
            return [[random.choice([0, 1]) for _ in range(size)]]
        else:
            layers = []
            for _ in range(depth):
                layer = []
                for _ in range(size):
                    if random.random() < 0.5:
                        layer.append(random.choice(generate_ac0_circuit(1, size)))
                    else:
                        layer.append([random.choice(layer) for _ in range(size)])
                layers.append(layer)
            return layers
    
    def simulate_circuit(circuit):
        n = len(circuit[0])
        truth_table = [0] * (2**n)
        for i in range(2**n):
            inputs = [(i >> j) & 1 for j in range(n)]
            value = circuit[0][inputs.index(inputs[0])]
            for layer in circuit[1:]:
                value = layer[value]
            truth_table[i] = value
        return truth_table
    
    def symmetrization(truth_table, n):
        g_f = [0] * (n + 1)
        for k in range(n + 1):
            count = sum(1 for x in range(2**n) if bin(x).count('1') == k)
            g_f[k] = sum(truth_table[x] for x in range(2**n) if bin(x).count('1') == k) / count
        return g_f
    
    def compute_psi_sym(g_f, n):
        def objective(k, q):
            return max(abs(q[j] - g_f[j]) for j in range(n + 1))
        
        def constraints(k):
            A = [[0 for _ in range(k + 1)] for _ in range(n + 1)]
            b = [0] * (n + 1)
            for j in range(n + 1):
                A[j][j] = 1
                b[j] = g_f[j]
            return A, b
        
        k_min = 0
        k_max = n
        while k_min < k_max:
            k_mid = (k_min + k_max) // 2
            A, b = constraints(k_mid)
            res = linprog([1], A_ub=A, b_ub=b, bounds=(None, None), method='highs')
            if res.success and res.fun <= 1/3:
                k_min = k_mid + 1
            else:
                k_max = k_mid
        
        return k_min - 1
    
    def parity_function(n):
        g_parity = [0] * (n + 1)
        for k in range(n + 1):
            count = sum(1 for x in range(2**n) if bin(x).count('1') == k)
            g_parity[k] = (-1)**k
        return g_parity
    
    n_values = [8, 12, 16, 20, 24, 28, 32, 36, 40]
    d_values = [2, 3]
    s_values = [n**2 for n in n_values]
    
    results = []
    for n, d, s in zip(n_values, d_values, s_values):
        circuit = generate_ac0_circuit(d, s)
        truth_table = simulate_circuit(circuit)
        g_f = symmetrization(truth_table, n)
        
        psi_sym = compute_psi_sym(g_f, n)
        results.append(psi_sym)
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value)**2 for x in results) / len(results))
    
    conjecture_holds = all(x <= 8 * (math.log2(s))**(d-1) for s, d, x in zip(s_values, d_values, results))
    counterexample = "" if conjecture_holds else "psi_sym > 8 * (log_2 s)^(d-1)"
    
    return {
        "metric_name": "psi_sym",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"psi_sym > 8 * (log_2 s)^(d-1)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")