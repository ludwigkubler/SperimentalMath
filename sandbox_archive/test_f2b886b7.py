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
    
    def padic_order(f):
        # Placeholder for actual p-adic order calculation
        return 1
    
    def entropy(f):
        count = [f(x).count(0), f(x).count(1)]
        if sum(count) == 0:
            return 0
        p0, p1 = count[0] / sum(count), count[1] / sum(count)
        return -p0 * math.log2(p0) - p1 * math.log2(p1)
    
    def generate_boolean_function(n):
        return lambda x: [random.choice([0, 1]) for _ in range(n)]
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    ord_f = padic_order(f)
    ent_f = entropy(f)
    
    if ent_f == 0:
        return {
            "metric_name": "ord(padic_order(f)) / H(f)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = ord_f / ent_f
    
    return {
        "metric_name": "ord(padic_order(f)) / H(f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 10,  # Placeholder constant c
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if all(val is not None for val in results):
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
        support_fraction = sum(1 for val in results if val <= 10) / len(results)  # Placeholder constant c
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, val in enumerate(results) if val is None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")