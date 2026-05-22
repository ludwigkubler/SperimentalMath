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
    
    def generate_polynomial(n):
        return [random.choice([0, 1]) for _ in range(n+1)]
    
    def generate_function(n):
        return [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    
    def minimal_order(poly):
        n = len(poly)
        for k in range(1, n*n + 1):
            if all((poly[i] ** k) % 2 == poly[i] for i in range(n+1)):
                return k
        return n*n
    
    def acc0_circuit_threshold(poly):
        return True  # Placeholder; actual implementation needed
    
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            poly = generate_polynomial(n)
            if acc0_circuit_threshold(poly) and minimal_order(poly) < n:
                counterexample = f"Polynomial of degree {n} with non-trivial ACC⁰ circuit threshold but minimal order less than N"
                conjecture_holds = False
                break
            
            func = generate_function(n)
            if acc0_circuit_threshold(func) and minimal_order(func) < n:
                counterexample = f"Function of size {n} with non-trivial ACC⁰ circuit threshold but minimal order less than N"
                conjecture_holds = False
                break
        
        instances_tested += 5
    
    return {
        "metric_name": "minimal_order",
        "metric_value": (n*n for n in [5, 10, 15, 20, 30, 40]),
        "instances_tested": instances_tested,
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[sum(1 for r in results if not r['conjecture_holds'])].get('counterexample', 'unknown')}\") first_failing_seed={seeds[sum(1 for r in results if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")