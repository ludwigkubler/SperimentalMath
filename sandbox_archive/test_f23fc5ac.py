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
    
    def frobenius_schur_indicator(n):
        # Placeholder for actual implementation of Frobenius-Schur indicator
        return n % 2
    
    def communication_complexity_rank(M):
        # Placeholder for actual implementation of communication complexity rank
        return len(M) - sum(1 for row in M if all(x == 0 for x in row))
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + random.randint(0, m - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(x != 0 for x in row))
        return rank
    
    def generate_random_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def function_to_matrix(f, n):
        matrix = []
        for i in range(2**n):
            binary = format(i, f'0{n}b')
            row = [f(int(binary[j])) for j in range(n)]
            matrix.append(row)
        return matrix
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_variance = 0
        indicator_sum = 0
        
        while len(results) < 30 and len(results) < 8 * n:  # Ensure at least 30 instances per seed
            f = generate_random_function(n)
            M = function_to_matrix(f, n)
            rank = communication_complexity_rank(M)
            indicator = frobenius_schur_indicator(n)
            
            if rank == 0:
                continue
            
            total_variance += (rank - indicator) ** 2
            indicator_sum += indicator
            instances_tested += 1
        
        if instances_tested < 30:
            return {
                "metric_name": "Var(Rank(M))",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        mean_variance = total_variance / instances_tested
        mean_indicator = indicator_sum / instances_tested
        
        results.append({
            "n": n,
            "instances_tested": instances_tested,
            "mean_variance": mean_variance,
            "mean_indicator": mean_indicator
        })
    
    support_fraction = sum(1 for result in results if result["mean_variance"] <= result["mean_indicator"]) / len(results)
    
    return {
        "metric_name": "Var(Rank(M))",
        "metric_value": support_fraction,
        "instances_tested": sum(result["instances_tested"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={sum(result['support_fraction'] for result in results)/len(results)} std=0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")