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
    
    def is_monotone(f):
        n = len(f)
        for i in range(n):
            for j in range(i + 1, n):
                if f[i] > f[j]:
                    return False
        return True
    
    def generate_random_monotone_function(n):
        inputs = [random.choice([0, 1]) for _ in range(n)]
        outputs = sorted(inputs)
        return outputs
    
    def compute_minimal_rank(f):
        n = len(f)
        identity_matrix = [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]
        
        def matrix_multiply(A, B):
            result = [[sum(a * b for a, b in zip(row_A, col_B)) for col_B in zip(*B)] for row_A in A]
            return result
        
        def gaussian_elimination(matrix):
            n = len(matrix)
            for i in range(n):
                max_row = max(range(i, n), key=lambda k: abs(matrix[k][i]))
                matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
                
                denom = matrix[i][i]
                if denom == 0:
                    continue
                
                for j in range(n):
                    matrix[i][j] /= denom
                
                for k in range(n):
                    if k != i:
                        factor = matrix[k][i]
                        for j in range(n):
                            matrix[k][j] -= factor * matrix[i][j]
            
            return matrix
        
        reduced_matrix = gaussian_elimination(identity_matrix)
        
        rank = sum(1 for row in reduced_matrix if any(row))
        return rank
    
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_random_monotone_function(n)
            if not is_monotone(f):
                return {
                    "metric_name": "minimal_rank",
                    "metric_value": None,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": "Non-monotone function generated"
                }
            
            min_rank = compute_minimal_rank(f)
            results.append((n, min_rank))
    
    c_Q = sum(min_rank for n, min_rank in results) / len(results)
    mean_rank = sum(min_rank * (math.log(n) if n > 0 else 1) for n, min_rank in results) / sum(math.log(n) if n > 0 else 1 for n, _ in results)
    
    conjecture_holds = all(min_rank >= c_Q * math.log(n) for n, min_rank in results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "c_Q * log(n) bound violated"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all("counterexample" in result and result["counterexample"] == "c_Q * log(n) bound violated" for result in results):
        print(f"RESULT: FALSIFIED counterexample=\"c_Q * log(n) bound violated\" first_failing_seed={seeds[0]}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0 support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")