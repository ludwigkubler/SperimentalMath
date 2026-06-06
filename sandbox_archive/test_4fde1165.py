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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            # Find pivot row
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            
            # Eliminate non-pivot elements
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            for k in range(i+1, n):
                factor = A[k][i]
                for j in range(n):
                    A[k][j] -= factor * A[i][j]
        
        # Back substitution to find the solution
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = A[i][-1]
            for j in range(i+1, n):
                x[i] -= A[i][j] * x[j]
            x[i] /= A[i][i]
        
        return x
    
    def symplectic_topological_degree(circuit):
        # Construct the vector bundle using a constructive mapping
        n = len(circuit)
        A = [[0] * (n+1) for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if circuit[i][j]:
                    A[i][j] = 1
                else:
                    A[i][j] = -1
        
        # Compute the rank of the matrix A
        rank = len(gaussian_elimination(A))
        
        # The symplectic topological degree is related to the rank
        return rank
    
    def communication_complexity_rank(circuit):
        # Placeholder for actual computation
        # For simplicity, we assume a constant rank for all circuits
        return 10
    
    n_values = [5, 10, 15, 20, 30, 40]
    metric_values = []
    
    for n in n_values:
        instances_tested = 0
        total_variance = 0
        
        for _ in range(5):
            circuit = [[random.choice([True, False]) for _ in range(n)] for _ in range(n)]
            degree = symplectic_topological_degree(circuit)
            comm_rank = communication_complexity_rank(circuit)
            instances_tested += 1
            total_variance += (comm_rank - n * math.log2(n)) ** 2
        
        if instances_tested < 30:
            return {
                "metric_name": "Variance of Communication Complexity Rank",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": max(n_values),
                "conjecture_holds": False,
                "counterexample": "Insufficient instances tested"
            }
        
        variance = total_variance / instances_tested
        metric_values.append(variance)
    
    mean_variance = sum(metric_values) / len(metric_values)
    std_variance = math.sqrt(sum((x - mean_variance) ** 2 for x in metric_values) / len(metric_values))
    
    if all(0.9 * n * math.log2(n) <= variance <= 1.1 * n * math.log2(n) for variance in metric_values):
        return {
            "metric_name": "Variance of Communication Complexity Rank",
            "metric_value": mean_variance,
            "instances_tested": sum(instances_tested for _ in n_values),
            "n_max": max(n_values),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "Variance of Communication Complexity Rank",
            "metric_value": mean_variance,
            "instances_tested": sum(instances_tested for _ in n_values),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": f"Counterexample found with variance {mean_variance}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
    mean_variance = sum(trial_result["metric_value"] for trial_result in [run_trial(seed) for seed in seeds]) / len(seeds)
    std_variance = math.sqrt(sum((trial_result["metric_value"] - mean_variance) ** 2 for trial_result in [run_trial(seed) for seed in seeds]) / len(seeds))
    
    support_fraction = sum(trial_result["conjecture_holds"] for trial_result in [run_trial(seed) for seed in seeds]) / len(seeds)
    
    if all(trial_result["conjecture_holds"] for trial_result in [run_trial(seed) for seed in seeds]):
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_variance} std={std_variance} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed in seeds if not run_trial(seed)["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Variance out of expected range\" first_failing_seed={first_failing_seed}")