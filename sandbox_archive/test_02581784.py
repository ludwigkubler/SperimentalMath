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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        # Find pivot row
        max_row = i
        for j in range(i+1, n):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below the pivot
        factor = Fraction(A[i][i])
        for j in range(i, n):
            A[i][j] /= factor
        
        for k in range(n):
            if k != i:
                factor = Fraction(A[k][i])
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    return [row[i:] for row in A]

def compute_rho(G):
    n = len(G)
    adjacency_matrix = [[0] * n for _ in range(n)]
    for u, v in G:
        adjacency_matrix[u][v] = 1
        adjacency_matrix[v][u] = 1
    
    # Convert to augmented matrix and perform Gaussian elimination
    A = [row + [1] for row in adjacency_matrix]
    rank = len(gaussian_elimination(A))
    
    return rank

def brute_force_xor_circuit(n):
    if n == 1:
        return 1
    circuit_size = float('inf')
    for i in range(2**n):
        circuit = []
        for j in range(n-1):
            circuit.append((i & (1 << j)) ^ (i & (1 << (j+1))))
        if all(circuit[k] == (circuit[k-1] ^ circuit[k-2]) for k in range(2, n)):
            circuit_size = min(circuit_size, len(circuit))
    return circuit_size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random graph with n vertices
    n = random.randint(5, 40)
    G = []
    for _ in range(n * (n - 1) // 2):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v and (u, v) not in G and (v, u) not in G:
            G.append((u, v))
    
    # Compute the minimal rank ρ(G)
    rho_G = compute_rho(G)
    
    # Compute the XOR circuit size
    xor_circuit_size = brute_force_xor_circuit(n)
    
    # Check if the conjecture holds for this seed
    if rho_G >= 10 and xor_circuit_size >= 100:
        return {
            "metric_name": "XOR circuit size",
            "metric_value": xor_circuit_size,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"rho(G) >= 10"
        }
    
    # Check the correlation between ρ(G) and XOR circuit size
    if abs(xor_circuit_size - (1 / rho_G)**2) <= 3:
        return {
            "metric_name": "XOR circuit size",
            "metric_value": xor_circuit_size,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    
    return {
        "metric_name": "XOR circuit size",
        "metric_value": xor_circuit_size,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": f"rho(G) = {rho_G}, XOR circuit size = {xor_circuit_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    # Compute mean/std of metric_value and fraction of seeds where conjecture_holds
    total_metric_value = sum(r["metric_value"] for r in results)
    total_instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_metric_value = total_metric_value / total_instances_tested
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / total_instances_tested)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False and "rho(G) >= 10" in r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["conjecture_holds"] is False and "rho(G) >= 10" in r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample='rho(G) >= 10' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")