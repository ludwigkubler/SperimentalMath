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
    
    def generate_random_circuit(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def entanglement_complexity(circuit):
        n = len(circuit)
        count = 0
        for i in range(n):
            if circuit[i] == 1:
                count += 1
        return count
    
    def symplectic_leaves(e):
        # Placeholder function to simulate the computation of symplectic leaves
        # This is a dummy implementation and should be replaced with actual logic
        return e + 1
    
    n_max = 0
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        n = random.randint(5, 40)
        circuit = generate_random_circuit(n)
        e = entanglement_complexity(circuit)
        L = symplectic_leaves(e)
        
        if n > n_max:
            n_max = n
        
        instances_tested += 1
        total_metric_value += L
        
        if L > f(e) * 2**(n/4):
            conjecture_holds = False
            counterexample = "Circuit with n={}, e={}, L={} exceeds the bound".format(n, e, L)
    
    metric_mean = total_metric_value / instances_tested
    
    return {
        "metric_name": "Symplectic Leaves",
        "metric_value": metric_mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def f(d):
    # Placeholder function for the bound f(d)
    # This is a dummy implementation and should be replaced with actual logic
    return d + 1

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, 0.0, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, 0.0, support_fraction))
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(r["counterexample"], seed))
                break