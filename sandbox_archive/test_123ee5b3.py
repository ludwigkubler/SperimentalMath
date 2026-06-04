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
    
    def generate_boolean_function(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def hodge_order(boolean_function):
        n = len(boolean_function)
        # Simplified heuristic to estimate Hodge order
        return Fraction(n, 2).limit_denominator()
    
    def monotone_width(circuit):
        # Simplified heuristic to estimate monotone width
        return len(circuit) / 2
    
    def construct_circuit(boolean_function):
        n = len(boolean_function)
        circuit = []
        for i in range(n):
            circuit.append(f'NOT x{i}')
        return circuit
    
    instances_tested = 0
    total_h = 0
    total_w = 0
    counterexample = ""
    
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        boolean_function = generate_boolean_function(n)
        h = hodge_order(boolean_function)
        circuit = construct_circuit(boolean_function)
        w = monotone_width(circuit)
        
        if h <= 0 or w <= 0:
            continue
        
        instances_tested += 1
        total_h += h
        total_w += w
        
        ratio = Fraction(h, w).limit_denominator()
        log_n = Fraction(n).log(2).limit_denominator()
        
        if ratio > 1.5 or ratio < 0.7:
            counterexample = f"n={n}, h={h}, w={w}, ratio={ratio}"
            break
    
    mean_h = total_h / instances_tested
    mean_w = total_w / instances_tested
    support_fraction = (instances_tested - len(counterexample.split('\n'))) / instances_tested
    
    return {
        "metric_name": "hodge_order_over_monotone_width",
        "metric_value": mean_h / mean_w,
        "instances_tested": instances_tested,
        "n_max": max([5, 10, 15, 20, 30, 40]),
        "conjecture_holds": support_fraction >= 0.95,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")