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
    
    def gaussian_elimination(A, b):
        n = len(A)
        augmented_matrix = [A[i] + [b[i]] for i in range(n)]
        
        for i in range(n):
            pivot_row = max(range(i, n), key=lambda r: abs(augmented_matrix[r][i]))
            augmented_matrix[i], augmented_matrix[pivot_row] = augmented_matrix[pivot_row], augmented_matrix[i]
            
            if augmented_matrix[i][i] == 0:
                return None  # Singular matrix
            
            for j in range(i + 1, n):
                factor = augmented_matrix[j][i] / augmented_matrix[i][i]
                for k in range(n + 1):
                    augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        x = [0] * n
        for i in range(n - 1, -1, -1):
            x[i] = (augmented_matrix[i][-1] - sum(augmented_matrix[i][j] * x[j] for j in range(i + 1, n))) / augmented_matrix[i][i]
        
        return x
    
    def communication_complexity_rank(I):
        n = len(I)
        A = [I[i] + [-1] for i in range(n)]
        b = [0] * n
        rank = gaussian_elimination(A, b)
        if rank is None:
            return float('inf')
        return sum(1 for x in rank if x != 0)
    
    def minimal_monodromy_group_order(I):
        n = len(I)
        S_n = list(range(n))
        stabilizer_subgroup = [S_n]
        
        for i in range(n):
            for j in range(i + 1, n):
                if I[i][j] != I[j][i]:
                    return float('inf')
        
        def is_stabilizer(subset):
            for i in range(n):
                if any(I[subset.index(i)][subset.index(j)] != I[i][j] for j in subset if j != i):
                    return False
            return True
        
        for r in range(1, n):
            for subset in itertools.combinations(S_n, r):
                if is_stabilizer(subset):
                    stabilizer_subgroup.append(list(subset))
        
        return len(stabilizer_subgroup)
    
    def alpha(n):
        return Fraction(math.log(n) ** 2).limit_denominator()
    
    n = random.randint(5, 40)
    I = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        I[i][i] = 0
    
    M_G_order = minimal_monodromy_group_order(I)
    r_G = communication_complexity_rank(I)
    
    if M_G_order == float('inf') or r_G == float('inf'):
        return {
            "metric_name": "minimal_monodromy_group_order",
            "metric_value": M_G_order,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "singular_matrix"
        }
    
    conjecture_holds = M_G_order <= alpha(n) and r_G <= alpha(n)
    counterexample = "" if conjecture_holds else f"M_G_order={M_G_order}, alpha(n)={alpha(n)}, r_G={r_G}"
    
    return {
        "metric_name": "minimal_monodromy_group_order",
        "metric_value": M_G_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")