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

def generate_boolean_circuit(n, w):
    if n <= 1 or w <= 1:
        return []
    circuit = []
    for _ in range(w):
        layer = [random.choice([0, 1]) for _ in range(n)]
        circuit.append(layer)
    return circuit

def construct_orbifold_manifold(circuit):
    # Simplified model: each gate is a vertex and edges represent connections
    n = len(circuit[0])
    m = len(circuit)
    vertices = set(range(n * m))
    edges = []
    for i in range(m):
        for j in range(n):
            if circuit[i][j] == 1:
                if i > 0:
                    edges.append((i * n + j, (i - 1) * n + j))
                if i < m - 1:
                    edges.append((i * n + j, (i + 1) * n + j))
                if j > 0:
                    edges.append((i * n + j, i * n + j - 1))
                if j < n - 1:
                    edges.append((i * n + j, i * n + j + 1))
    return vertices, edges

def euler_characteristic(vertices, edges):
    return len(vertices) - len(edges)

def satisfiability_time(circuit):
    # Simplified model: time is proportional to the number of gates
    return len(circuit[0]) * len(circuit)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            circuit = generate_boolean_circuit(n, random.randint(1, n))
            vertices, edges = construct_orbifold_manifold(circuit)
            chi = euler_characteristic(vertices, edges)
            t_s = satisfiability_time(circuit)
            results.append((chi, t_s))
    
    if not results:
        return {
            "metric_name": "Euler Characteristic vs Satisfiability Time",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    chi_values = [r[0] for r in results]
    t_s_values = [r[1] for r in results]
    mean_chi = sum(chi_values) / len(chi_values)
    mean_t_s = sum(t_s_values) / len(t_s_values)
    correlation_coefficient = (sum((chi - mean_chi) * (t_s - mean_t_s) for chi, t_s in results) /
                               math.sqrt(sum((chi - mean_chi) ** 2 for chi in chi_values) *
                                         sum((t_s - mean_t_s) ** 2 for t_s in t_s_values)))
    
    return {
        "metric_name": "Euler Characteristic vs Satisfiability Time",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.5,  # Threshold for linear correlation
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(30)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(results)}")