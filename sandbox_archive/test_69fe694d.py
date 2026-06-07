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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def local_cohomology(f, q):
        n = len(f)
        F_q = list(range(q))
        H_f = []
        
        for x in F_q:
            if f[x.index(0)] == 1:
                H_f.append(x)
        
        return H_f
    
    def communication_matrix(f, q):
        n = len(f)
        F_q = list(range(q))
        M = [[0] * (q**n) for _ in range(q**n)]
        
        for x in F_q:
            for y in F_q:
                if f[x.index(0)] == 1 and f[y.index(0)] == 1:
                    M[x][y] += 1
        
        return M
    
    def rank_variance(M):
        n = len(M)
        total_sum = sum(sum(row) for row in M)
        mean = Fraction(total_sum, n**2)
        
        variance = 0
        for i in range(n):
            for j in range(n):
                variance += (M[i][j] - mean)**2
        
        return math.sqrt(variance / n**2)
    
    def pearson_correlation(X, Y):
        n = len(X)
        mean_X = sum(X) / n
        mean_Y = sum(Y) / n
        
        cov = 0
        for i in range(n):
            cov += (X[i] - mean_X) * (Y[i] - mean_Y)
        
        std_X = math.sqrt(sum((x - mean_X)**2 for x in X) / n)
        std_Y = math.sqrt(sum((y - mean_Y)**2 for y in Y) / n)
        
        return cov / (std_X * std_Y)
    
    def min_local_cohomology(H_f):
        if not H_f:
            return 0
        return min(len(x) for x in H_f)
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        q = random.randint(2, 10)
        
        H_f = local_cohomology(f, q)
        M = communication_matrix(f, q)
        sigma_rank = rank_variance(M)
        min_H_f = min_local_cohomology(H_f)
        
        results.append((min_H_f, sigma_rank))
    
    correlation_coefficient = pearson_correlation([x for x, _ in results], [y for _, y in results])
    
    return {
        "metric_name": "Pearson's Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")