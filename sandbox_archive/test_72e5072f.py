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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_characteristic_function(f):
        n = int(math.log2(len(f)))
        X = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == 1 and f[j] == 1:
                    X[i][j] = 1
        return X
    
    def compute_norm(X):
        norm = 0
        for row in X:
            for val in row:
                norm += val ** 2
        return math.sqrt(norm)
    
    def compute_influence_complexity(f, n):
        influence = [0] * n
        for i in range(n):
            f_prime = f[:]
            f_prime[i] = 1 - f_prime[i]
            if f_prime != f:
                influence[i] += abs(sum(f) / sum(f_prime))
        return max(influence)
    
    def correlation(X, Y):
        mean_X = sum(X) / len(X)
        mean_Y = sum(Y) / len(Y)
        cov = sum((x - mean_X) * (y - mean_Y) for x, y in zip(X, Y)) / len(X)
        var_X = sum((x - mean_X) ** 2 for x in X) / len(X)
        var_Y = sum((y - mean_Y) ** 2 for y in Y) / len(Y)
        return cov / (math.sqrt(var_X) * math.sqrt(var_Y))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_corr = 0
        
        for _ in range(5):  # Ensure at least 5 instances per size
            f = generate_boolean_function(n)
            X = compute_characteristic_function(f)
            norm = compute_norm(X)
            influence_complexity = compute_influence_complexity(f, n)
            
            if norm == 0:
                continue
            
            corr = correlation([norm**2] * len(influence_complexity), influence_complexity)
            total_corr += corr
            instances_tested += 1
        
        if instances_tested > 0:
            avg_corr = total_corr / instances_tested
            results.append(avg_corr)
    
    if not results:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    avg_corr = sum(results) / len(results)
    support_fraction = sum(1 for corr in results if corr > 0.7) / len(results)
    
    return {
        "metric_name": "correlation",
        "metric_value": avg_corr,
        "instances_tested": sum(len(results)),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    if all(result is not None for result in results):
        mean_corr = sum(results) / len(results)
        support_fraction = sum(1 for corr in results if corr > 0.7) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std={math.sqrt(sum((x - mean_corr) ** 2 for x in results) / len(results))} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='support_fraction < 0.8' first_failing_seed={seeds[next(i for i, corr in enumerate(results) if corr <= 0.7)]}")
    else:
        print("RESULT: INCONCLUSIVE some results are None")