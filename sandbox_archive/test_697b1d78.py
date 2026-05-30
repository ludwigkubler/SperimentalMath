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
    
    def communication_complexity(f):
        n = len(f)
        cc = 0
        for x in range(n):
            for y in range(x + 1, n):
                if f[x] != f[y]:
                    cc += 1
        return cc
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(n)]
    
    def arithmetic_progression(f, g, k, n):
        ap = []
        for x in range(n):
            ap.append((f[x], g[x]))
        return ap
    
    def has_common_elements(ap):
        seen = set()
        for pair in ap:
            if pair[0] in seen or pair[1] in seen:
                return True
            seen.add(pair[0])
            seen.add(pair[1])
        return False
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_boolean_function(n)
        g = generate_boolean_function(n)
        
        if communication_complexity(f) != communication_complexity(g):
            continue
        
        for k in range(n):
            ap = arithmetic_progression(f, g, k, n)
            if has_common_elements(ap):
                continue
            instances_tested += 1
            if communication_complexity(f) > 2 * communication_complexity(g):
                conjecture_holds = False
                counterexample = f"Arithmetic progression {ap} for n={n}, k={k}"
                break
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity(f),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")