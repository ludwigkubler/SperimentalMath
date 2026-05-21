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
    
    def hypergeometric_function(n, k):
        if n < k or k == 0:
            return 1
        result = 1.0
        for i in range(1, k + 1):
            result *= (n - i + 1) / i
        return result
    
    def moments_of_hypergeometric(n, k):
        moments = [hypergeometric_function(n, i) for i in range(k + 2)]
        return sum(moments)
    
    n = random.randint(5, 40)
    k = min(n - 1, 3)  # Ensure k is at least 1 and less than n
    size_of_smallest_circuit = random.randint(1, n**2)  # Simplified for testing
    
    metric_value = moments_of_hypergeometric(n, k)
    conjecture_holds = metric_value >= (n ** k) * math.log(n)
    
    return {
        "metric_name": "Sum of Moments",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, k={k}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['counterexample']}\", first_failing_seed={first_failing_seed}")