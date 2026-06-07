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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def fourier_coefficients(f):
        n = int(math.log2(len(f)))
        coeffs = [0] * (2*n + 1)
        for i in range(len(f)):
            for j in range(2*n + 1):
                angle = 2 * math.pi * j * i / len(f)
                coeffs[j] += f[i] * math.cos(angle) / len(f)
        return coeffs
    
    def geometric_measure(coeffs):
        sum_of_squares = sum(x**2 for x in coeffs)
        return math.sqrt(sum_of_squares)
    
    def communication_complexity_rank(M):
        n, m = len(M), len(M[0])
        rank = 0
        for i in range(n):
            if M[i][i] != 0:
                rank += 1
                for j in range(i+1, n):
                    M[j][i] /= M[i][i]
                    for k in range(m):
                        M[j][k] -= M[j][i] * M[i][k]
        return rank
    
    def matrix_representation(f):
        n = int(math.log2(len(f)))
        M = [[0] * (n+1) for _ in range(n+1)]
        for i in range(2**n):
            binary_rep = format(i, f'0{n}b')
            for j in range(n):
                if binary_rep[j] == '1':
                    M[j][j+1] += 1
                else:
                    M[j+1][j] += 1
        return M
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, n_max + 1):
        f = generate_boolean_function(n)
        coeffs = fourier_coefficients(f)
        geo_measure = geometric_measure(coeffs)
        M = matrix_representation(f)
        rank = communication_complexity_rank(M)
        
        if geo_measure == 0 or rank == 0:
            continue
        
        metric_values.append(geo_measure * rank)
    
    if len(metric_values) < instances_tested:
        conjecture_holds = False
        counterexample = "not_enough_instances"
    
    return {
        "metric_name": "GeoMeasure * Rank",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": len(metric_values),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[sum(1 for r in results if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")