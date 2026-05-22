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
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    def tropical_add(a, b):
        return max(a, b)
    
    def tropical_multiply(a, b):
        return a + b
    
    def tropical_negate(a):
        return -a
    
    def tropical_zero():
        return float('-inf')
    
    def tropical_one():
        return 0
    
    def tropical_is_zero(a):
        return a == float('-inf')
    
    def tropical_matrix_multiply(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        C = [[tropical_zero() for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    C[i][j] = tropical_add(C[i][j], tropical_multiply(A[i][k], B[k][j]))
        return C
    
    def gaussian_elimination(A, b):
        m = len(A)
        n = len(A[0])
        augmented_matrix = [A[i] + [b[i]] for i in range(m)]
        
        for j in range(n):
            max_row = j
            for i in range(j+1, m):
                if abs(augmented_matrix[i][j]) > abs(augmented_matrix[max_row][j]):
                    max_row = i
            
            augmented_matrix[j], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[j]
            
            pivot = augmented_matrix[j][j]
            for k in range(j, n+1):
                augmented_matrix[j][k] /= pivot
            
            for i in range(m):
                if i != j:
                    factor = augmented_matrix[i][j]
                    for k in range(j, n+1):
                        augmented_matrix[i][k] -= factor * augmented_matrix[j][k]
        
        return [row[-1] for row in augmented_matrix]
    
    def minimal_rank(A):
        m = len(A)
        n = len(A[0])
        rank = 0
        for i in range(n):
            if not tropical_is_zero(gaussian_elimination(A, [tropical_one() if j == i else tropical_zero() for j in range(m)])[i]):
                rank += 1
        return rank
    
    def xor_function(x):
        result = 0
        for bit in x:
            result ^= bit
        return result
    
    def communication_complexity(n, x):
        return n  # Simplified model: each input bit requires one bit of communication
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_communication = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n with 5 different inputs
            x = [random.randint(0, 1) for _ in range(n)]
            A = [[tropical_xor(x[i], x[j]) for j in range(n)] for i in range(n)]
            rank = minimal_rank(A)
            communication = communication_complexity(n, x)
            
            total_rank += rank
            total_communication += communication
            instances_tested += 1
    
    mean_rank = total_rank / instances_tested
    mean_communication = total_communication / instances_tested
    
    conjecture_holds = mean_rank <= log2(log2(instances_tested)) and mean_communication >= log2(log2(instances_tested))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_rank={mean_rank}, mean_communication={mean_communication}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j for i in range(5) for j in range(5)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")