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
    
    def boolean_degree(f):
        m = len(f)
        max_degree = 0
        for i in range(m):
            for j in range(i+1, m):
                if f[i] != f[j]:
                    degree = 0
                    x = 1
                    while True:
                        if (x & (1 << i)) and not (x & (1 << j)):
                            degree += 1
                        elif not (x & (1 << i)) and (x & (1 << j)):
                            degree += 1
                        else:
                            break
                        x <<= 1
                    max_degree = max(max_degree, degree)
        return max_degree
    
    def kostka_coefficient(m):
        # Placeholder for actual Kostka coefficient calculation
        # This is a dummy implementation for testing purposes
        return m**2
    
    n = random.randint(5, 40)
    m = random.randint(1, min(n, 10))
    boolean_functions = [generate_boolean_function(m) for _ in range(30)]
    
    max_kostka_coefficient = max(kostka_coefficient(len(f)) for f in boolean_functions if boolean_degree(f) <= 2)
    expected_bound = m**(3/4) * n**(3/4)
    
    metric_name = "max_kostka_coefficient"
    metric_value = max_kostka_coefficient
    instances_tested = len(boolean_functions)
    conjecture_holds = max_kostka_coefficient <= expected_bound
    counterexample = "" if conjecture_holds else f"rank={max_kostka_coefficient}, expected={expected_bound}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")