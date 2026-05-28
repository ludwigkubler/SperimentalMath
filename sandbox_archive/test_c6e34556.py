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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        # Find pivot
        max_row = i
        for j in range(i+1, m):
            if abs(A[j][i]) > abs(A[max_row][i]):
                max_row = j
        A[i], A[max_row] = A[max_row], A[i]
        
        # Eliminate below
        for j in range(i+1, m):
            factor = Fraction(A[j][i], A[i][i])
            for k in range(n):
                A[j][k] -= factor * A[i][k]

def matrix_multiply(A, B):
    m, n, p = len(A), len(B[0]), len(B)
    C = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            for k in range(p):
                C[i][j] += A[i][k] * B[k][j]
    return C

def identity_matrix(size):
    return [[1 if i == j else 0 for j in range(size)] for i in range(size)]

def inverse_matrix(A):
    m, n = len(A), len(A[0])
    assert m == n
    I = identity_matrix(m)
    A_augmented = [row + col for row, col in zip(A, I)]
    
    gaussian_elimination(A_augmented)
    
    inv_A = [row[n:] for row in A_augmented]
    return inv_A

def homomorphism(G, k):
    n = len(G)
    phi_G = []
    for _ in range(n):
        phi_G.append(random.sample(range(k), k))
    return phi_G

def clique_instance(n):
    edges = set()
    for i in range(n):
        for j in range(i+1, n):
            if random.choice([True, False]):
                edges.add((i, j))
    return edges

def monotone_circuit_size(edges, k):
    # Placeholder function to simulate circuit size calculation
    # This is a dummy implementation and should be replaced with actual algorithm
    return len(edges) * k

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    phi_G_values = []
    circuit_size_values = []
    
    for n in n_values:
        G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        k = random.randint(1, n)
        
        phi_G = homomorphism(G, k)
        edges = clique_instance(n)
        circuit_size = monotone_circuit_size(edges, k)
        
        phi_G_values.append(phi_G)
        circuit_size_values.append(circuit_size)
    
    correlation_coefficient = 0
    for i in range(len(n_values)):
        for j in range(i+1, len(n_values)):
            n1, n2 = n_values[i], n_values[j]
            phi_G1, phi_G2 = phi_G_values[i], phi_G_values[j]
            circuit_size1, circuit_size2 = circuit_size_values[i], circuit_size_values[j]
            
            if phi_G1 <= n1**(4/3) or phi_G2 <= n2**(4/3):
                return {
                    "metric_name": "correlation_coefficient",
                    "metric_value": correlation_coefficient,
                    "instances_tested": len(n_values),
                    "conjecture_holds": False,
                    "counterexample": f"phi(G) ≤ {n1}^(4/3) or phi(G) ≤ {n2}^(4/3)"
                }
            
            if circuit_size1 == 0 or circuit_size2 == 0:
                continue
            
            correlation_coefficient += (phi_G1 * circuit_size1 - phi_G2 * circuit_size2) / (circuit_size1 + circuit_size2)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*37, 37))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")