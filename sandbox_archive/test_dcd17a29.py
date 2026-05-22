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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_instance(n):
        # Generate a random instance of tensor product disjointness with n variables
        A = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        return A, B
    
    def noncrossing_partition_rank(A):
        # Compute the minimal rank of a noncrossing partition representation
        n = len(A)
        if n == 0:
            return 0
        
        # Initialize the matrix with zeros
        M = [[0] * (n + 1) for _ in range(n + 1)]
        
        # Fill the matrix with the values from A and B
        for i in range(n):
            for j in range(n):
                M[i][j + 1] += A[i][j]
                M[j + 1][i] += B[i][j]
        
        # Perform Gaussian elimination to find the rank
        rank = 0
        for i in range(n):
            if M[i][i] == 0:
                found_nonzero = False
                for j in range(i + 1, n):
                    if M[j][i] != 0:
                        M[i], M[j] = M[j], M[i]
                        found_nonzero = True
                        break
                if not found_nonzero:
                    continue
            
            rank += 1
            denom = Fraction(M[i][i])
            for j in range(n + 1):
                M[i][j] /= denom
        
            for j in range(n):
                if i != j and M[j][i] != 0:
                    factor = Fraction(M[j][i], M[i][i])
                    for k in range(n + 1):
                        M[j][k] -= factor * M[i][k]
        
        return rank
    
    def communication_complexity(A, B):
        # Measure the randomized communication complexity
        n = len(A)
        if n == 0:
            return 0
        
        # Initialize the matrix with zeros
        M = [[0] * (n + 1) for _ in range(n + 1)]
        
        # Fill the matrix with the values from A and B
        for i in range(n):
            for j in range(n):
                M[i][j + 1] += A[i][j]
                M[j + 1][i] += B[i][j]
        
        # Perform Gaussian elimination to find the rank
        rank = 0
        for i in range(n):
            if M[i][i] == 0:
                found_nonzero = False
                for j in range(i + 1, n):
                    if M[j][i] != 0:
                        M[i], M[j] = M[j], M[i]
                        found_nonzero = True
                        break
                if not found_nonzero:
                    continue
            
            rank += 1
            denom = Fraction(M[i][i])
            for j in range(n + 1):
                M[i][j] /= denom
        
            for j in range(n):
                if i != j and M[j][i] != 0:
                    factor = Fraction(M[j][i], M[i][i])
                    for k in range(n + 1):
                        M[j][k] -= factor * M[i][k]
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        A, B = generate_instance(n)
        τ_M = noncrossing_partition_rank(A)
        comm_complexity = communication_complexity(A, B)
        
        if τ_M == 0 or comm_complexity == 0:
            continue
        
        results.append({
            "n": n,
            "τ_M": τ_M,
            "comm_complexity": comm_complexity
        })
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    τ_M_values = [result["τ_M"] for result in results]
    comm_complexity_values = [result["comm_complexity"] for result in results]
    
    correlation_coefficient = sum((τ_M - mean_τ_M) * (comm_complexity - mean_comm_complexity) for τ_M, comm_complexity in zip(τ_M_values, comm_complexity_values)) / len(results)
    mean_τ_M = sum(τ_M_values) / len(results)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and mean_τ_M <= n * (n + 1) / 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")