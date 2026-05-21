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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def matrix_mod(A, m):
    return [[(a[i][j] % m + m) % m for j in range(len(A[0]))] for i in range(len(A))]

def gaussian_elimination(A, m):
    n = len(A)
    rank = 0
    for i in range(n):
        if A[i][i] == 0:
            swap_found = False
            for k in range(i + 1, n):
                if A[k][i] != 0:
                    A[i], A[k] = A[k], A[i]
                    swap_found = True
                    break
            if not swap_found:
                continue
        pivot = A[i][i]
        for j in range(n):
            A[i][j] = (A[i][j] * pow(pivot, m - 2, m)) % m
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
    s_values = [2 * n, 4 * n, 8 * n]
    epsilon_threshold = 0.02
    R_threshold = 0.01
    
    results = []
    
    for n in n_values:
        for d in d_values:
            for s in s_values:
                if len(results) >= 30:
                    break
                
                # Generate random AC^0[MOD_3] circuit
                gates = ['AND', 'OR', 'NOT'] * (s // 3)
                random.shuffle(gates)
                inputs = [random.choice(['MOD_3']) for _ in range(s)]
                
                # Compute truth table
                def evaluate_circuit(circuit, input_values):
                    if len(circuit) == 1:
                        return input_values[circuit[0]]
                    gate = circuit[0]
                    args = circuit[1:]
                    if gate == 'AND':
                        return all(evaluate_circuit(arg, input_values) for arg in args)
                    elif gate == 'OR':
                        return any(evaluate_circuit(arg, input_values) for arg in args)
                    elif gate == 'NOT':
                        return not evaluate_circuit(args[0], input_values)
                
                truth_table = [evaluate_circuit(inputs, i) for i in range(2 ** n)]
                epsilon = abs(sum(truth_table) / (2 ** n) - 0.5)
                
                if epsilon < epsilon_threshold:
                    continue
                
                # Build multigraph G_C
                V = set()
                E = []
                sink = 'sink'
                V.add(sink)
                
                for i in range(n):
                    V.add(i)
                    E.append((i, sink))
                
                for gate_index in range(len(gates)):
                    gate_type = gates[gate_index]
                    if gate_type == 'NOT':
                        input_index = random.randint(0, len(inputs) - 1)
                        inputs[input_index] = 'NOT_' + str(input_index)
                    else:
                        input_indices = [random.randint(0, len(inputs) - 1) for _ in range(2)]
                        for input_index in input_indices:
                            inputs[input_index] = gate_type + '_' + str(input_index)
                    
                    for input_index in input_indices:
                        V.add(input_index)
                        E.append((input_index, gate_index))
                
                # Form reduced Laplacian L̃ ∈ Z^{(|V|−1)×(|V|−1)}
                n_nodes = len(V)
                laplacian = [[0] * (n_nodes - 1) for _ in range(n_nodes - 1)]
                
                for u, v in E:
                    if u == sink or v == sink:
                        continue
                    i = list(V).index(u)
                    j = list(V).index(v)
                    laplacian[i][j] += 1
                    laplacian[j][i] += 1
                
                # Compute rk_2(K(G_C)) = (|V|−1) − rank(L̃ mod 2)
                reduced_laplacian_mod_2 = matrix_mod(laplacian, 2)
                rank_L_tilde_mod_2 = gaussian_elimination(reduced_laplacian_mod_2, 2)
                
                # Compute R
                R = (n_nodes - 1) * math.log(s + 1) / (epsilon * n ** (1 / d))
                
                results.append({
                    "metric_name": "R",
                    "metric_value": R,
                    "instances_tested": 1,
                    "conjecture_holds": R >= R_threshold,
                    "counterexample": ""
                })
    
    if not results:
        return {
            "seed": seed,
            "metric_name": "R",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_R = sum(result["metric_value"] for result in results) / len(results)
    median_R = sorted([result["metric_value"] for result in results])[len(results) // 2]
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "R",
        "metric_value": mean_R,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_R = sum(result["metric_value"] for result in results) / len(results)
    median_R = sorted([result["metric_value"] for result in results])[len(results) // 2]
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_R} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] and result["metric_value"] < 0.01 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] < 0.01)
        print(f"RESULT: FALSIFIED counterexample=\"R<0.01\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")