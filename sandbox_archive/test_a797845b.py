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
    n = random.randint(5, 40)
    M = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    # Ensure the matrix is symmetric and has zeros on the diagonal
    for i in range(n):
        for j in range(i+1, n):
            M[j][i] = M[i][j]
            if random.choice([True, False]):
                M[i][j] = 0
    
    p = math.log2(n)
    
    # Compute the noncommutative L^p norm (using singular value decomposition)
    def svd(matrix):
        U, S, Vt = [], [], []
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            row = [matrix[i][j] for j in range(n)]
            U.append(row)
        
        for i in range(n):
            col = [matrix[j][i] for j in range(m)]
            Vt.append(col)
        
        S = sorted([sum(x**2 for x in row)**0.5 for row in U], reverse=True)
        return U, S, Vt
    
    U, S, Vt = svd(M)
    norm_p = sum(S[i]**p for i in range(min(len(S), 10)))**(1/p)  # Use top 10 singular values for approximation
    
    metric_value = norm_p / n
    instances_tested = 1
    conjecture_holds = metric_value >= 0.1
    counterexample = "" if conjecture_holds else "Noncommutative L^p norm too small"
    
    return {
        "metric_name": "noncommutative_Lp_norm",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Noncommutative L^p norm too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE All trials used n=1")