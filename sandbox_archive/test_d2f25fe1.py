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
    
    # Define a function to generate a random d-dimensional vector space over a finite field F
    def generate_vector_space(d, q):
        V = []
        for _ in range(d):
            v = [random.randint(0, q-1) for _ in range(q)]
            V.append(v)
        return V
    
    # Define a function to compute the symplectic Laplacian matrix L_S(V)
    def symplectic_laplacian(V):
        d = len(V)
        L_S = [[0] * d for _ in range(d)]
        for i in range(d):
            for j in range(i+1, d):
                L_S[i][j] = V[j][i] - V[i][j]
                L_S[j][i] = -L_S[i][j]
        return L_S
    
    # Define a function to compute the eigenvalues of a matrix
    def eigenvalues(matrix):
        n = len(matrix)
        if n == 1:
            return [matrix[0][0]]
        
        # Gaussian elimination
        for i in range(n):
            pivot = matrix[i][i]
            if pivot == 0:
                continue
            for j in range(i+1, n):
                factor = matrix[j][i] / pivot
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        
        # Extract eigenvalues from the diagonal
        return [matrix[i][i] for i in range(n)]
    
    # Define a function to compute the communication complexity rank r(V)
    def communication_complexity_rank(V):
        d = len(V)
        q = len(V[0])
        rank = 0
        for v in V:
            if sum(v) != 0:
                rank += 1
        return rank
    
    # Parameters
    d = random.randint(5, 30)
    q = random.randint(2, 8)
    
    # Generate the vector space
    V = generate_vector_space(d, q)
    
    # Compute the symplectic Laplacian matrix
    L_S = symplectic_laplacian(V)
    
    # Compute the eigenvalues of L_S
    eigenvals = eigenvalues(L_S)
    lambda_min = min(eigenval for eigenval in eigenvals if eigenval != 0)
    
    # Compute the communication complexity rank r(V)
    r_V = communication_complexity_rank(V)
    
    # Perform Pearson correlation test
    mean_lambda_min = sum(lambda_min for _ in range(10)) / 10
    std_lambda_min = math.sqrt(sum((lambda_min - mean_lambda_min) ** 2 for _ in range(10)) / 9)
    mean_r_V = sum(r_V for _ in range(10)) / 10
    std_r_V = math.sqrt(sum((r_V - mean_r_V) ** 2 for _ in range(10)) / 9)
    
    n = len(eigenvals)
    numerator = sum((lambda_min[i] - mean_lambda_min) * (r_V[i] - mean_r_V) for i in range(n))
    denominator = std_lambda_min * std_r_V
    correlation_coefficient = numerator / denominator if denominator != 0 else 0
    
    # Check significance with p-value threshold of 0.05
    t_statistic = abs(correlation_coefficient) * math.sqrt((n - 2) / (1 - correlation_coefficient ** 2))
    p_value = 2 * (1 - math.erf(t_statistic / math.sqrt(2)))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 10,
        "n_max": d,
        "conjecture_holds": p_value >= 0.05,
        "counterexample": "" if p_value >= 0.05 else f"p-value={p_value} < 0.05"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / (len(results) - 1))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")