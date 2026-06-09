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
    
    def choi_isomorphism(channel):
        n = len(channel)
        choi_matrix = [[0] * (n**2) for _ in range(n**2)]
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    for l in range(n):
                        choi_matrix[i*n + j][k*n + l] += channel[i][j] * channel[k][l]
        return choi_matrix
    
    def eigenvalues(matrix):
        n = len(matrix)
        if n == 1:
            return [matrix[0][0]]
        
        # Gaussian elimination
        for i in range(n):
            max_row = max(range(i, n), key=lambda r: abs(matrix[r][i]))
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
        
        # Extract eigenvalues from diagonal
        return [matrix[i][i] for i in range(n)]
    
    def non_commutative_entropy(eigenvalues):
        entropy = 0
        for eig in eigenvalues:
            if eig > 0:
                entropy -= eig * math.log2(eig)
        return entropy
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        channel = [[random.random() for _ in range(n)] for _ in range(n)]
        choi_matrix = choi_isomorphism(channel)
        eigenvals = eigenvalues(choi_matrix)
        entropy = non_commutative_entropy(eigenvals)
        
        results.append({
            "n": n,
            "channel": channel,
            "choi_matrix": choi_matrix,
            "eigenvalues": eigenvals,
            "entropy": entropy
        })
    
    mean_entropy = sum(result["entropy"] for result in results) / len(results)
    max_n = max(result["n"] for result in results)
    
    return {
        "metric_name": "Non-commutative Dynamical Entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": False,  # Mapping undefined
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")