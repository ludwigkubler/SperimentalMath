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
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        instances_tested = 0
        cc_r = 0
        for i in range(2**n):
            for j in range(2**n):
                if f[i] != f[j]:
                    cc_r += 1
                    instances_tested += 1
        return cc_r / instances_tested
    
    def symplectic_leaves(f):
        n = int(math.log2(len(f)))
        leaves = set()
        for i in range(2**n):
            leaf = tuple(f[i])
            if leaf not in leaves:
                leaves.add(leaf)
        return len(leaves)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested_total = 0
    n_max = 0
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        cc_r = communication_complexity(f)
        L_f = symplectic_leaves(f)
        
        if n > n_max:
            n_max = n
        
        total_metric_value += math.log2(1 + cc_r)
        instances_tested_total += 1
    
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        f = generate_random_boolean_function(n)
        cc_r = communication_complexity(f)
        L_f = symplectic_leaves(f)
        
        if L_f > math.log2(2**n):
            conjecture_holds = False
            counterexample = f"Function with n={n} inputs has {L_f} leaves, which exceeds the upper bound of {math.log2(2**n)}"
    
    return {
        "metric_name": "log2(1 + CC_R(f))",
        "metric_value": total_metric_value / len(n_values),
        "instances_tested": instances_tested_total,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Default to first 10 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence to support or refute the conjecture")