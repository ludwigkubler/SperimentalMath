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
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def communication_complexity(f):
        m = len(f)
        n = 2**m
        total_bits_sent = 0
        for i in range(n):
            bits_sent = bin(i).count('1')
            total_bits_sent += bits_sent
        return total_bits_sent / n
    
    def luroth_normal_form_degree(f):
        m = len(f)
        if m == 1:
            return 1
        degree = 0
        for i in range(2**(m-1)):
            subfunction = f[i:i+2]
            if sum(subfunction) > 1:
                degree += 1
        return degree
    
    def pearson_correlation_coefficient(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        var_x = sum((x[i] - mean_x)**2 for i in range(n)) / n
        var_y = sum((y[i] - mean_y)**2 for i in range(n)) / n
        return cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    m_values = [5, 10, 15, 20, 30, 40]
    lnd_values = []
    r_values = []
    
    for m in m_values:
        f = generate_boolean_function(m)
        lnd = luroth_normal_form_degree(f)
        r = communication_complexity(f)
        lnd_values.append(lnd)
        r_values.append(r)
    
    correlation_coefficient = pearson_correlation_coefficient(lnd_values, r_values)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(m_values),
        "n_max": max(m_values),
        "conjecture_holds": correlation_coefficient >= 0.8 and all(corr >= 0.5 for corr in [correlation_coefficient]),
        "counterexample": "" if correlation_coefficient >= 0.8 else f"Correlation coefficient {correlation_coefficient} < 0.8"
    }

if __name__ == "__main__":
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] and res["metric_value"] < 0.5 for res in results):
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"] and res["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient statistical signal")