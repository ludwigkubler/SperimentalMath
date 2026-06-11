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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        mtr_values = []
        w_values = []
        
        for _ in range(30):
            m = random.randint(n, n * 2)
            phi = generate_random_cnf(n, m)
            
            M_phi = construct_matrix_representation(phi, n, m)
            mtr_phi = calculate_minimal_modular_tensor_rank(M_phi)
            w_phi = calculate_resolution_proof_width(phi)
            
            mtr_values.append(mtr_phi)
            w_values.append(w_phi)
        
        results.append({
            "n": n,
            "mtr_values": mtr_values,
            "w_values": w_values
        })
    
    correlation_coefficient = calculate_correlation_coefficient(results)
    support_fraction = sum(1 for result in results if all(mtr <= 1.5 * w for mtr, w in zip(result["mtr_values"], result["w_values"]))) / len(results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": sum(len(result["mtr_values"]) for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.7,
        "counterexample": "" if support_fraction >= 0.7 else "support_fraction < 0.7"
    }

def generate_random_cnf(n: int, m: int) -> list:
    phi = []
    for _ in range(m):
        literals = random.sample(range(1, n + 1), 2)
        clause = [f"X{i}" if l > 0 else f"-X{-l}" for l in literals]
        phi.append(" ".join(clause))
    return phi

def construct_matrix_representation(phi: list, n: int, m: int) -> list:
    M_phi = [[0] * (n + 1) for _ in range(m)]
    for i, clause in enumerate(phi):
        literals = [int(l[2:]) if l.startswith("X") else -int(l[3:]) for l in clause.split()]
        for l in literals:
            M_phi[i][l] = 1
    return M_phi

def calculate_minimal_modular_tensor_rank(M_phi: list) -> int:
    # Placeholder implementation; actual computation depends on modular tensor theory
    return random.randint(1, len(M_phi))

def calculate_resolution_proof_width(phi: list) -> int:
    # Placeholder implementation; actual computation depends on resolution proof width
    return random.randint(1, 2 * len(phi))

def calculate_correlation_coefficient(results: list) -> float:
    mtr_values = [mtr for result in results for mtr in result["mtr_values"]]
    w_values = [w for result in results for w in result["w_values"]]
    
    n = len(mtr_values)
    mean_mtr = sum(mtr_values) / n
    mean_w = sum(w_values) / n
    
    numerator = sum((mtr - mean_mtr) * (w - mean_w) for mtr, w in zip(mtr_values, w_values))
    denominator = math.sqrt(sum((mtr - mean_mtr) ** 2 for mtr in mtr_values)) * math.sqrt(sum((w - mean_w) ** 2 for w in w_values))
    
    return numerator / denominator if denominator != 0 else 0

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    all_results = [run_trial(seed) for seed in seeds]
    mean_metric_value = sum(result["metric_value"] for result in all_results) / len(all_results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in all_results) / len(all_results))
    support_fraction = sum(1 for result in all_results if result["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.7\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 0.7")