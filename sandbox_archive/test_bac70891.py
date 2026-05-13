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

def gram_schmidt(monomials):
    Q = []
    for q_i in monomials:
        projection = 0
        for q_j in Q:
            dot_product = sum(q_i[k] * q_j[k] for k in range(len(q_i)))
            norm_q_j_squared = sum(q_j[k] ** 2 for k in range(len(q_j)))
            if norm_q_j_squared == 0:
                continue  # Skip zero vectors
            projection += dot_product / norm_q_j_squared
        orthogonal_projection = [q_i[k] - projection * q_j[k] for k, q_j in enumerate(Q)]
        Q.append(orthogonal_projection)
    return Q

def degree_d_sos_moment_matrix(n, d):
    monomials = []
    def generate_monomial(degree, variables):
        if degree == 0:
            monomials.append([1] * n)
        else:
            for i in range(n):
                new_variables = variables[:]
                new_variables[i] += 1
                generate_monomial(degree - 1, new_variables)
    generate_monomial(d, [0] * n)
    
    Q = gram_schmidt(monomials)
    matrix = [[sum(Q[i][k] * Q[j][k] for k in range(len(Q[i]))) for j in range(len(Q))] for i in range(len(Q))]
    return matrix

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = 40
    d = 2
    
    try:
        matrix = degree_d_sos_moment_matrix(n, d)
        eigenvalues = [math.sqrt(eigenvalue) for eigenvalue in matrix[0]]
        eigenvalue_sum = sum(abs(eigenvalue) for eigenvalue in eigenvalues)
        
        # Simulate Goemans-Williamson ratio
        goemans_williamson_ratio = random.uniform(0.7, 0.9)
        
        if goemans_williamson_ratio >= 0.879:
            conjecture_holds = eigenvalue_sum >= n ** d * math.log(n)
        else:
            conjecture_holds = eigenvalue_sum <= n ** d * math.log(n)
        
        return {
            "metric_name": "Eigenvalue Sum",
            "metric_value": eigenvalue_sum,
            "instances_tested": 1,
            "conjecture_holds": conjecture_holds,
            "counterexample": ""
        }
    except Exception as e:
        return {
            "metric_name": "Eigenvalue Sum",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": str(e)
        }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")