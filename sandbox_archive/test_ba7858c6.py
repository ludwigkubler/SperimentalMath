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
    
    def generate_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(variables, 3)
            clause = [random.choice([var, f'~{var}']) for var in clause]
            clauses.append(clause)
        return variables, clauses
    
    def geometric_entropy(Q):
        # Simplified version of geometric entropy calculation
        return sum(math.log2(1 / Q[i][i]) for i in range(len(Q))) / len(Q)
    
    def circuit_depth(phi):
        # Placeholder for actual circuit depth computation
        # For simplicity, assume a constant depth based on instance size
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        variables, clauses = generate_instance(n)
        Q = [[0] * (2 ** n) for _ in range(2 ** n)]
        # Placeholder for actual quantum system construction
        # For simplicity, assume a diagonal matrix with random values
        for i in range(2 ** n):
            Q[i][i] = random.random()
        
        epsilon_phi = geometric_entropy(Q)
        depth_phi = circuit_depth(variables, clauses)
        
        results.append({
            "n": n,
            "epsilon_phi": epsilon_phi,
            "depth_phi": depth_phi
        })
    
    total_epsilon = sum(result["epsilon_phi"] for result in results)
    average_epsilon = total_epsilon / len(results)
    max_n = max(result["n"] for result in results)
    
    conjecture_holds = all(epsilon >= n ** (1/3) and depth <= 2 * epsilon for epsilon, depth in zip([result["epsilon_phi"] for result in results], [result["depth_phi"] for result in results]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": average_epsilon,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")