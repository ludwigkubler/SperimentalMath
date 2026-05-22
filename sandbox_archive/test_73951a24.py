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
    
    def p_adic_derivative(f):
        n = int(math.log2(len(f)))
        df = [0] * len(f)
        for i in range(1, n + 1):
            mask = (1 << i) - 1
            for j in range(2**(n-i)):
                x = j | mask
                y = j & ~mask
                df[x] += f[y]
        return [x / len(f) for x in df]
    
    def circuit_complexity(f):
        n = int(math.log2(len(f)))
        if n == 0:
            return 1
        count = 0
        for i in range(1, n + 1):
            mask = (1 << i) - 1
            for j in range(2**(n-i)):
                x = j | mask
                y = j & ~mask
                if f[x] != f[y]:
                    count += 1
        return count
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        df = p_adic_derivative(f)
        cc = circuit_complexity(f)
        
        if len(df) != len(f):
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "p_adic_derivative_length_mismatch"
            }
        
        if cc == 0:
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": 0,
                "conjecture_holds": False,
                "counterexample": "circuit_complexity_zero"
            }
        
        correlation = sum(x * y for x, y in zip(df, f)) / (len(f) * cc)
        results.append({
            "n": n,
            "correlation_coefficient": correlation
        })
    
    mean_correlation = sum(r["correlation_coefficient"] for r in results) / len(results)
    std_deviation = math.sqrt(sum((r["correlation_coefficient"] - mean_correlation)**2 for r in results) / len(results))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_correlation,
        "instances_tested": 6 * len(n_values),
        "conjecture_holds": mean_correlation >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r) / len(results)
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if "metric_value" in r) / len(results))
    support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_deviation} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if 'counterexample' in r)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")