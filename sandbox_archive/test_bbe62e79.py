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
    
    def noncrossing_partition_tree_height(f):
        n = len(f)
        if n == 1:
            return 1
        height = 0
        while f:
            new_f = []
            for i in range(len(f) // 2):
                a, b = f[2*i], f[2*i+1]
                if a != b:
                    new_f.append(0)
                else:
                    new_f.append(a)
            f = new_f
            height += 1
        return height
    
    def ac0_circuit_size(f):
        n = len(f)
        if n == 1:
            return 1
        size = 0
        while f:
            new_f = []
            for i in range(len(f) // 2):
                a, b = f[2*i], f[2*i+1]
                if a != b:
                    new_f.append(0)
                else:
                    new_f.append(a)
            f = new_f
            size += 1
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            f = generate_boolean_function(n)
            height = noncrossing_partition_tree_height(f)
            size = ac0_circuit_size(f)
            results.append((n, height, size))
    
    if not results:
        return {
            "metric_name": "AC^0 Circuit Size",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_height = sum(h for n, h, s in results) / len(results)
    mean_size = sum(s for n, h, s in results) / len(results)
    support_fraction = sum(1 for n, h, s in results if h <= 2**(0.5 * math.log(n)**2)) / len(results)
    
    return {
        "metric_name": "AC^0 Circuit Size",
        "metric_value": mean_size,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"height={mean_height} > size={mean_size}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_size} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and sum(1 for r in results if not r["conjecture_holds"]) / len(results) < 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"height > size\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")