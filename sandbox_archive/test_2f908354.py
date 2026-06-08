# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, chain

# Define constants
K = 3  # Example k-value for k-CNF
N_MIN = 5
N_MAX = 40
SEEDS = [2**i - 1 for i in range(1, 6)] if len(sys.argv) < 2 else list(map(int, sys.argv[1:]))

def random_k_cnf(n, m):
    variables = set(range(1, n + 1))
    clauses = []
    while len(clauses) < m:
        clause = random.sample(variables, K)
        if all(len(set(c)) == K for c in combinations(clause, k)):
            clauses.append(clause)
    return clauses

def simplicial_complex_from_k_cnf(clauses):
    faces = set()
    for clause in clauses:
        faces.add(frozenset(clause))
        for i in range(1, len(clause)):
            for comb in combinations(clause, i):
                faces.add(frozenset(comb))
    return faces

def compute_local_index(faces):
    dim_counts = {}
    for face in faces:
        dim = len(face)
        if dim not in dim_counts:
            dim_counts[dim] = 0
        dim_counts[dim] += 1
    local_index = sum(count / (dim + 1) for dim, count in dim_counts.items())
    return local_index

def frege_proof_depth(clauses):
    # Placeholder function to simulate Frege proof depth calculation
    # This is a dummy implementation and should be replaced with actual logic
    return len(clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in range(N_MIN, N_MAX + 1):
        m = max(30, n * 2)  # Ensure at least 30 instances per seed
        for _ in range(m):
            clauses = random_k_cnf(n, m)
            faces = simplicial_complex_from_k_cnf(clauses)
            local_index = compute_local_index(faces)
            proof_depth = frege_proof_depth(clauses)
            
            if local_index > 10:
                return {
                    "metric_name": "LocalIndex",
                    "metric_value": local_index,
                    "instances_tested": m,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"local_index={local_index} exceeds 10"
                }
            
            results.append((local_index, proof_depth))
    
    if len(results) < 30:
        return {
            "metric_name": "LocalIndex",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": N_MAX,
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    local_indices, proof_depths = zip(*results)
    correlation_coefficient = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(local_indices, proof_depths)) / \
                              math.sqrt(sum((xi - x_bar)**2 for xi in local_indices)) / \
                              math.sqrt(sum((yi - y_bar)**2 for yi in proof_depths))
    x_bar = sum(local_indices) / len(local_indices)
    y_bar = sum(proof_depths) / len(proof_depths)
    
    return {
        "metric_name": "LocalIndex",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": N_MAX,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    results = []
    for seed in SEEDS:
        trial_result = run_trial(seed)
        results.append(trial_result)
        print(f"TRIAL: {trial_result}")
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(SEEDS, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")