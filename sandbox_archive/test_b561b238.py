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
    
    def generate_disjointness_matrix(n):
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            M[i][i] = 1
        return M
    
    def eigenvalues(matrix):
        n = len(matrix)
        if n == 1:
            return [matrix[0][0]]
        
        # Compute the characteristic polynomial using cofactor expansion
        det = 0
        for j in range(n):
            minor = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1) ** j * matrix[0][j] * determinant(minor)
        return [det]
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        elif n == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        
        det = 0
        for j in range(n):
            minor = [[matrix[i][k] for k in range(n) if k != j] for i in range(1, n)]
            det += (-1) ** j * matrix[0][j] * determinant(minor)
        return det
    
    def logarithmic_potential(eigs):
        return sum(math.log(abs(eig)) for eig in eigs)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    M = generate_disjointness_matrix(n)
    eigs = eigenvalues(M)
    free_entropy = logarithmic_potential(eigs)
    
    return {
        "metric_name": "free_entropy",
        "metric_value": free_entropy,
        "instances_tested": n,
        "conjecture_holds": free_entropy >= n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_free_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_free_entropy = math.sqrt(sum((r["metric_value"] - mean_free_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_free_entropy} std={std_free_entropy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"free entropy < n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")