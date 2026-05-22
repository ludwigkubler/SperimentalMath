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
    
    def boolean_function_to_permutation(f):
        n = len(f(0))  # Assuming f is a function that takes an integer and returns a tuple of length n
        return [f(i).index(1) for i in range(n)]
    
    def tensor_rank(permutation):
        n = len(permutation)
        if n == 1:
            return 1
        rank = 0
        for i in range(n):
            sub_permutation = permutation[:i] + permutation[i+1:]
            if len(set(sub_permutation)) < len(sub_permutation):
                continue
            rank += 1
        return rank
    
    def min_representation_rank(f):
        n = len(f(0))
        matroid = []
        for i in range(n):
            row = [f(j)[i] for j in range(n)]
            matroid.append(row)
        rank = 0
        while True:
            if all(all(matroid[i][j] == 0 for j in range(rank)) for i in range(rank)):
                break
            rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = lambda x: tuple(random.randint(0, 1) for _ in range(n))
        permutation = boolean_function_to_permutation(f)
        tau_n = tensor_rank(permutation)
        rho_f = min_representation_rank(f)
        
        if tau_n == 0 or rho_f == 0:
            continue
        
        results.append({
            "n": n,
            "tau_n": tau_n,
            "rho_f": rho_f
        })
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    tau_ns = [result["tau_n"] for result in results]
    rho_fs = [result["rho_f"] for result in results]
    
    correlation_coefficient = sum((tau_ns[i] - mean(tau_ns)) * (rho_fs[i] - mean(rho_fs)) for i in range(len(results))) / (len(results) * std(tau_ns) * std(rho_fs))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

def mean(values):
    return sum(values) / len(values)

def std(values):
    avg = mean(values)
    return math.sqrt(sum((x - avg) ** 2 for x in values) / len(values))

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
    
    correlation_coefficients = [run_trial(seed)["metric_value"] for seed in seeds if run_trial(seed)["metric_value"] is not None]
    
    if all(correlation >= 0.8 for correlation in correlation_coefficients) and len([correlation for correlation in correlation_coefficients if correlation < 0.5]) == 0:
        print(f"RESULT: SUPPORTED mean={mean(correlation_coefficients)} std={std(correlation_coefficients)} support_fraction=1.0")
    elif any(correlation < 0.5 for correlation in correlation_coefficients):
        first_failing_seed = seeds[correlation_coefficients.index(min([correlation for correlation in correlation_coefficients if correlation < 0.5]))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")