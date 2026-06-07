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

def matrix_multiply(A, B):
    m, k = len(A), len(B[0])
    n = len(B)
    C = [[0] * k for _ in range(m)]
    for i in range(m):
        for j in range(k):
            for l in range(n):
                C[i][j] += A[i][l] * B[l][j]
    return C

def gaussian_elimination(A, b):
    n = len(b)
    M = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(M[j][i]) > abs(M[max_row][i]):
                max_row = j
        M[i], M[max_row] = M[max_row], M[i]
        pivot = M[i][i]
        for j in range(i, n + 1):
            M[i][j] /= pivot
        for j in range(n):
            if j != i:
                factor = M[j][i]
                for k in range(i, n + 1):
                    M[j][k] -= factor * M[i][k]
    return [row[-1] for row in M]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_lattice(n):
        lattice = [[random.randint(-n, n) for _ in range(n)] for _ in range(n)]
        return lattice
    
    def generate_xor_circuit(n):
        circuit = [random.choice([0, 1]) for _ in range(2**n)]
        return circuit
    
    def orbit_diameter(lattice):
        n = len(lattice)
        distances = []
        for i in range(n):
            for j in range(i+1, n):
                dist = sum(abs(lattice[i][k] - lattice[j][k]) for k in range(n))
                distances.append(dist)
        return max(distances) if distances else 0
    
    def entanglement_complexity(circuit):
        n = int(math.log2(len(circuit)))
        complexity = 0
        for i in range(2**n):
            state = [circuit[i]] + [random.choice([0, 1]) for _ in range(n-1)]
            for j in range(i+1, 2**n):
                if circuit[j] == state[0]:
                    complexity += 1
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        lattice = generate_lattice(n)
        circuit = generate_xor_circuit(n)
        orbit_diam = orbit_diameter(lattice)
        entang_complexity_val = entanglement_complexity(circuit)
        results.append((orbit_diam, entang_complexity_val))
    
    if not results:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    orbit_diam_values = [r[0] for r in results]
    entang_complexity_values = [r[1] for r in results]
    
    mean_orbit_diam = sum(orbit_diam_values) / len(orbit_diam_values)
    mean_entang_complexity = sum(entang_complexity_values) / len(entang_complexity_values)
    
    covariance = sum((orbit_diam_values[i] - mean_orbit_diam) * (entang_complexity_values[i] - mean_entang_complexity) for i in range(len(orbit_diam_values)))
    variance_orbit_diam = sum((orbit_diam_values[i] - mean_orbit_diam)**2 for i in range(len(orbit_diam_values)))
    variance_entang_complexity = sum((entang_complexity_values[i] - mean_entang_complexity)**2 for i in range(len(entang_complexity_values)))
    
    if variance_orbit_diam == 0 or variance_entang_complexity == 0:
        return {
            "metric_name": "Pearson's correlation coefficient",
            "metric_value": None,
            "instances_tested": len(orbit_diam_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    pearsons_corr = covariance / math.sqrt(variance_orbit_diam * variance_entang_complexity)
    
    return {
        "metric_name": "Pearson's correlation coefficient",
        "metric_value": pearsons_corr,
        "instances_tested": len(orbit_diam_values),
        "n_max": max(n_values),
        "conjecture_holds": pearsons_corr >= 0.8,
        "counterexample": "" if pearsons_corr >= 0.8 else f"r={pearsons_corr:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_metric_value:.4f} std=NA support_fraction={support_fraction:.2f}"
    elif any(not r["conjecture_holds"] and "counterexample" not in r for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        result = f"FALSIFIED counterexample=\"Pearson's correlation coefficient < 0.8\" first_failing_seed=NA"
    
    print(result)