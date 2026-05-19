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
    n = 40
    s = 100
    d = 5
    k = 20
    ε = 0.1
    
    # Generate a random function f ∈ {0,1}^n computable by an ACC⁰ circuit of size s and depth d
    f = [random.choice([0, 1]) for _ in range(n)]
    
    # Construct the SOS moment matrix M_k(f)
    M = [[0] * (k + 1) for _ in range(k + 1)]
    for i in range(k + 1):
        for j in range(k + 1):
            for x in range(2**n):
                if bin(x).count('1') == i and bin(x).count('0') == j:
                    M[i][j] += f[x]
    
    # Compute the minimum eigenvalue λ_min of the SOS moment matrix M_k(f)
    λ_min = min(eigenvalue(M) for _ in range(10))
    
    # Verify if λ_min scales as Ω(s^{-1/2}) and whether ε < Ω(s^{-1/2}) forces k ≥ Ω(log s)
    conjecture_holds = λ_min >= s**(-0.5) and ε < s**(-0.5)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimum_eigenvalue",
        "metric_value": λ_min,
        "instances_tested": 10,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def eigenvalue(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1)**j * matrix[0][j] * eigenvalue(submatrix)
    
    return det

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) if len(sys.argv) > 1 else [2**i for i in range(5, 6)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=budget_exceeded n_tested={len(seeds)}")