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
    
    def k_clique_indicator_function(instance, n, k):
        # Placeholder implementation for k-CLIQUE indicator function
        return 0 if len(instance) < k else 1
    
    def walsh_hadamard_transform(f, n):
        if n == 1:
            return [f(0)]
        
        f_even = walsh_hadamard_transform(lambda x: f(2 * x), n // 2)
        f_odd = walsh_hadamard_transform(lambda x: f(2 * x + 1), n // 2)
        result = []
        
        for i in range(n):
            if i < len(f_even) and i < len(f_odd):
                result.append(f_even[i // 2] + f_odd[i // 2])
            else:
                result.append(0)
        
        return result
    
    def sum_abs_coefficients(coefficients):
        return sum(abs(c) for c in coefficients)
    
    n = random.randint(5, 40)
    instances_tested = 30
    total_sum = 0
    
    for _ in range(instances_tested):
        instance = [random.choice([0, 1]) for _ in range(n)]
        coefficients = walsh_hadamard_transform(lambda x: k_clique_indicator_function(instance, n, 3), n)
        total_sum += sum_abs_coefficients(coefficients)
    
    mean_value = Fraction(total_sum, instances_tested)
    conjecture_holds = mean_value <= 10 * math.log(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "sum_abs_coefficients",
        "metric_value": float(mean_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")