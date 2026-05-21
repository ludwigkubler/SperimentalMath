# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a*b) // gcd(a, b)

def matrix_mod(A, m):
    return [[(a[i][j] % m + m) % m for j in range(len(A[0]))] for i in range(len(A))]

def gaussian_elimination(A, m):
    n = len(A)
    rank = 0
    for i in range(n):
        if A[i][i] == 0:
            swap_found = False
            for k in range(i+1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    swap_found = True
                    break
            if not swap_found:
                continue
        pivot = A[i][i]
        for j in range(n):
            A[i][j] = (A[i][j] * pow(pivot, -1, m)) % m
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(n):
                    A[k][j] = (A[k][j] - factor * A[i][j]) % m
        rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [8, 10, 12, 14]
    d_values = [2, 3]
    s_values = [2*n, 4*n, 8*n]
    p = 3
    c = Fraction(1, 1)  # Placeholder for the absolute constant c
    
    results = []
    
    for n in n_values:
        for d in d_values:
            for s in s_values:
                if s < n or s % n != 0:
                    continue
                
                # Generate random AC^0[MOD_3] circuit
                gates = ['AND', 'OR', 'NOT'] * (s // n)
                random.shuffle(gates)
                
                # Compute truth table
                inputs = list(itertools.product([0, 1], repeat=n))
                outputs = [sum(inputs[i]) % p for i in range(len(inputs))]
                epsilon = abs(Fraction(sum(outputs), len(outputs)) - Fraction(1, 2))
                if epsilon < 0.02:
                    continue
                
                # Build multigraph G_C
                V = set()
                E = []
                
                for i in range(n):
                    V.add(f'input_{i}')
                
                def add_edge(u, v):
                    if (u, v) not in E and (v, u) not in E:
                        E.append((u, v))
                
                for gate in gates:
                    if gate == 'AND':
                        for i in range(n):
                            add_edge(f'input_{i}', f'gate_{gates.index(gate)}')
                        V.add(f'gate_{gates.index(gate)}')
                    elif gate == 'OR':
                        for i in range(n):
                            add_edge(f'input_{i}', f'gate_{gates.index(gate)}')
                        V.add(f'gate_{gates.index(gate)}')
                    elif gate == 'NOT':
                        add_edge(f'input_{n-1}', f'gate_{gates.index(gate)}')
                        V.add(f'gate_{gates.index(gate)}')
                
                V.add('sink')
                for i in range(n):
                    add_edge(f'gate_{len(gates)-1}', 'sink')
                
                # Form reduced Laplacian L̃ ∈ Z^{(|V|−1)×(|V|−1)}
                n_v = len(V)
                laplacian = [[0] * (n_v - 1) for _ in range(n_v - 1)]
                degree = [0] * n_v
                
                for u, v in E:
                    if u == 'sink' or v == 'sink':
                        continue
                    i = list(V).index(u)
                    j = list(V).index(v)
                    laplacian[i][j] -= 1
                    laplacian[j][i] -= 1
                    degree[i] += 1
                    degree[j] += 1
                
                for i in range(n_v - 1):
                    laplacian[i][i] = degree[list(V).index(list(V)[i])]
                
                # Compute rk_2(K(G_C)) = (|V|−1) − rank(L̃ mod 2)
                laplacian_mod_2 = matrix_mod(laplacian, 2)
                rank_laplace_mod_2 = gaussian_elimination(laplacian_mod_2, 2)
                rk_2_K = n_v - 1 - rank_laplace_mod_2
                
                # Compute test ratio R
                if epsilon >= 0.02:
                    R = rk_2_K * Fraction(n_v - 1).log(s + 1) / (epsilon * n ** (1/d))
                    results.append(R)
    
    if not results:
        return {
            "metric_name": "R",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    min_R = min(results)
    median_R = statistics.median(results)
    
    return {
        "metric_name": "R",
        "metric_value": median_R,
        "instances_tested": len(results),
        "conjecture_holds": min_R >= 0.01 and median_R >= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    import statistics
    
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        
        if "metric_value" in trial_result and trial_result["metric_value"] is not None:
            results.append(trial_result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE No valid instances found")
    else:
        mean_R = sum(results) / len(results)
        std_R = statistics.stdev(results)
        support_fraction = sum(1 for r in results if r >= 0.01 and r >= 0.1) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_R} std={std_R} support_fraction={support_fraction}")
        elif any(r < 0.01 for r in results):
            first_failing_seed = seeds[results.index(next(r for r in results if r < 0.01))]
            print(f"RESULT: FALSIFIED counterexample=\"R<0.01\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE support_fraction too low")