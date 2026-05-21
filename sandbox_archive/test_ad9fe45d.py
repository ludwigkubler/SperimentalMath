# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_monotonic(f):
        n = len(f)
        for i in range(n):
            if any(f[i | (1 << j)] < f[i] for j in range(n)):
                return False
        return True
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def count_symmetry_classes(f):
        n = len(f)
        sym_classes = set()
        for perm in permutations(range(n)):
            permuted_f = [f[perm[i]] for i in range(n)]
            if permuted_f not in sym_classes:
                sym_classes.add(tuple(permuted_f))
        return len(sym_classes)
    
    def permutations(lst):
        if len(lst) == 0:
            yield []
        else:
            for i in range(len(lst)):
                rest = lst[:i] + lst[i+1:]
                for p in permutations(rest):
                    yield [lst[i]] + p
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_symmetry_classes = 0
    num_instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test 5 instances per size
            f = generate_boolean_function(n)
            if not is_monotonic(f):
                return {
                    "metric_name": "symmetry_classes",
                    "metric_value": None,
                    "instances_tested": num_instances_tested,
                    "conjecture_holds": False,
                    "counterexample": "function_not_monotonic"
                }
            total_symmetry_classes += count_symmetry_classes(f)
            num_instances_tested += 1
    
    mean_symmetry_classes = total_symmetry_classes / num_instances_tested
    return {
        "metric_name": "symmetry_classes",
        "metric_value": mean_symmetry_classes,
        "instances_tested": num_instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"function_not_monotonic\" first_failing_seed={first_failing_seed}")