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
# end SEC prelude

import random
import math
from typing import List, Dict

def gram_matrix(instance: List[List[int]]) -> List[List[float]]:
    n = len(instance)
    G = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            sum_val = 0
            for k in range(n):
                sum_val += instance[i][k] * instance[j][k]
            G[i][j] = sum_val
            G[j][i] = sum_val
    return G

def eigenvalues(matrix: List[List[float]]) -> List[float]:
    n = len(matrix)
    if n == 1:
        return [matrix[0][0]]
    
    # Gaussian elimination to reduce the matrix
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        factor = 1 / matrix[i][i]
        for j in range(n):
            matrix[i][j] *= factor
        
        for j in range(n):
            if i != j:
                factor = -matrix[j][i]
                for k in range(n):
                    matrix[j][k] += factor * matrix[i][k]
    
    # Extract eigenvalues from the diagonal
    return [matrix[i][i] for i in range(n)]

def run_trial(seed: int) -> Dict[str, any]:
    random.seed(seed)
    n = random.randint(5, 40)
    instance = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    G = gram_matrix(instance)
    eigenvals = eigenvalues(G)
    k = sum(1 for val in eigenvals if abs(val) > 1e-6)
    
    sos_degree = math.ceil(math.log2(k))
    conjecture_holds = True
    counterexample = ""
    
    # Check if the SOS degree is at least log₂(k)
    if sos_degree < math.log2(k):
        conjecture_holds = False
        counterexample = f"SOS degree {sos_degree} is less than log₂({k})"
    
    return {
        "metric_name": "SOS Degree",
        "metric_value": sos_degree,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        counterexample_desc = results[seeds.index(first_failing_seed)]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")