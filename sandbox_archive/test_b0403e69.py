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
    
    def boolean_tensor_product_valuation(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function length must be a power of 2")
        return sum(f[i] * (1 << i) for i in range(n))
    
    def symplectic_cell_decomposition(f):
        n = int(math.log2(len(f)))
        if len(f) != 2**n:
            raise ValueError("Function length must be a power of 2")
        rank = 0
        for i in range(1, n):
            if all(f[j] == f[j + (1 << i)] for j in range(0, 2**(n - i), 2 * (1 << i))):
                rank += 1
        return rank
    
    def complexity_of_evaluation(f):
        return boolean_tensor_product_valuation(f)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    r_delta = symplectic_cell_decomposition(f)
    c_f = complexity_of_evaluation(f)
    
    if c_f == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "c_f is zero"
        }
    
    ratio = r_delta / c_f
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2.0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")