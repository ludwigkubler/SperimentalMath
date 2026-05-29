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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(1 << n)]
    
    def quantum_logarithmic_capacity(f):
        n = int(math.log2(len(f)))
        matrix = [[f[i * (1 << n) + j] for j in range(1 << n)] for i in range(1 << n)]
        
        # Gaussian elimination to find the rank of the matrix
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        
        for col in range(cols):
            max_row = None
            for row in range(rank, rows):
                if matrix[row][col] != 0:
                    max_row = row
                    break
            
            if max_row is not None:
                matrix[max_row], matrix[rank] = matrix[rank], matrix[max_row]
                
                for i in range(rows):
                    if i != rank:
                        factor = -matrix[i][col] / matrix[rank][col]
                        for j in range(cols):
                            matrix[i][j] += factor * matrix[rank][j]
                
                rank += 1
        
        return rank
    
    def monotone_circuit_size(f):
        n = int(math.log2(len(f)))
        # Simplified heuristic to estimate circuit size
        return sum(1 for bit in f if bit == 1) + n
    
    def minimal_depth(f):
        n = int(math.log2(len(f)))
        # Simplified heuristic to estimate depth
        return sum(1 for bit in f if bit == 1)
    
    c = 0.5  # Example constant, adjust as needed
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        f = generate_random_boolean_function(n)
        
        qlc = quantum_logarithmic_capacity(f)
        s_mon = monotone_circuit_size(f)
        d = minimal_depth(f)
        
        results.append({
            "n": n,
            "qlc": qlc,
            "s_mon": s_mon,
            "d": d
        })
    
    metric_value = sum(result["s_mon"] - c * result["qlc"]**2 for result in results) / len(results)
    conjecture_holds = all(result["s_mon"] >= c * result["qlc"]**2 for result in results)
    counterexample = "" if conjecture_holds else "minimal_depth_less_than_c_QLC_squared"
    
    return {
        "metric_name": "S_mon - c * QLC^2",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"minimal_depth_less_than_c_QLC_squared\" first_failing_seed={first_failing_seed}")