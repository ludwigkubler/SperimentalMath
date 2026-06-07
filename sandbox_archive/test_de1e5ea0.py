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
    
    def formal_power_series(circuit):
        n = len(circuit)
        if n == 0:
            return (2, [1])
        coeffs = [0] * (2**n)
        for i in range(2**n):
            term = 1
            for j in range(n):
                if (i >> j) & 1:
                    term *= circuit[j]
                else:
                    term *= 1 - circuit[j]
            coeffs[i] = term
        p = 2
        while True:
            valid = True
            for coeff in coeffs:
                if coeff % p == 0:
                    valid = False
                    break
            if valid:
                return (p, coeffs)
            p += 1
    
    def entanglement_complexity(circuit):
        n = len(circuit)
        complexity = 0
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i] != circuit[j]:
                    complexity += 1
        return complexity
    
    def f(n):
        return math.log2(n)**2
    
    max_n = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, max_n + 1):
        circuit = [random.choice([0, 1]) for _ in range(n)]
        p, coeffs = formal_power_series(circuit)
        complexity = entanglement_complexity(circuit)
        metric_value = f(complexity)
        if p > metric_value:
            conjecture_holds = False
            counterexample = f"Circuit with n={n} and complexity={complexity} has p-adic order {p}, which exceeds f(n)={metric_value}"
            break
        
        total_metric_value += metric_value
        instances_tested += 1
    
    return {
        "metric_name": "minimal_p_adic_order",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0.0,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61,
        67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")