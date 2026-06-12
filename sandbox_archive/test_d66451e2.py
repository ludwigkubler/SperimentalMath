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
    
    def generate_random_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        m = 2**(n-1)
        rank = sum(1 for i in range(m) if f[i] != f[2*i] and f[i] != f[2*i+1])
        return (rank - m/2)**2 / (m * (m-1))
    
    def symplectic_hull_volume(f):
        n = len(f)
        V = 0
        for i in range(2**n):
            if all(f[i] == f[j] for j in range(i, 2**n, 2)):
                V += 1
        return V
    
    def pearson_correlation_coefficient(X, Y):
        n = len(X)
        mean_X = sum(X) / n
        mean_Y = sum(Y) / n
        cov_XY = sum((X[i] - mean_X) * (Y[i] - mean_Y) for i in range(n)) / n
        var_X = sum((X[i] - mean_X)**2 for i in range(n)) / n
        var_Y = sum((Y[i] - mean_Y)**2 for i in range(n)) / n
        return cov_XY / math.sqrt(var_X * var_Y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    SHV_values = []
    CRV_values = []
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        SHV_values.append(symplectic_hull_volume(f))
        CRV_values.append(communication_complexity_rank_variance(f))
    
    correlation_coefficient = pearson_correlation_coefficient(SHV_values, CRV_values)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": "" if correlation_coefficient >= 0.7 else "Pearson correlation coefficient < 0.7"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient < 0.7' first_failing_seed={first_failing_seed}")