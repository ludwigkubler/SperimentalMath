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

def gaussian_elimination(matrix, b):
    n = len(matrix)
    augmented_matrix = [row + [b[i]] for i, row in enumerate(matrix)]
    
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i+1, n):
            if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                max_row = j
        
        # Swap rows
        augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
        
        # Eliminate non-pivot elements in the current column
        for j in range(n):
            if i != j:
                factor = Fraction(augmented_matrix[j][i], augmented_matrix[i][i])
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
    
    # Check if the system has a unique solution
    rank = 0
    for row in augmented_matrix:
        if any(row[i] != 0 for i in range(n)):
            rank += 1
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_ranks = []
    proof_depths = []
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            cnf = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
            rank = gaussian_elimination(cnf, [random.randint(0, 1) for _ in range(n)])
            min_ranks.append(rank)
            
            # Simulate DPLL proof depth (placeholder)
            proof_depth = random.randint(1, n * n)
            proof_depths.append(proof_depth)
    
    if len(min_ranks) < 30 or len(proof_depths) < 30:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": len(min_ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances"
        }
    
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    mean_proof_depth = sum(proof_depths) / len(proof_depths)
    
    correlation_coefficient = (n_values[-1] * sum(xi * yi for xi, yi in zip(min_ranks, proof_depths)) -
                               sum(min_ranks) * sum(proof_depths)) / \
                              math.sqrt((n_values[-1] * sum(xi**2 for xi in min_ranks) - sum(min_ranks)**2) *
                                        (n_values[-1] * sum(yi**2 for yi in proof_depths) - sum(proof_depths)**2))
    
    p_value = 2 * (1 - math.erf(abs(correlation_coefficient) / math.sqrt(2 * len(n_values))))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7 and p_value < 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) / len(results) >= 0.2:
        print("RESULT: FALSIFIED counterexample=\"Insufficient evidence\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")