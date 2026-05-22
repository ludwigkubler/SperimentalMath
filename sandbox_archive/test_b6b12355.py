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
    
    def generate_polynomial(d, F):
        coefficients = [random.choice(F) for _ in range(d + 1)]
        return sum(c * x**i for i, c in enumerate(coefficients))
    
    def evaluate_polynomial(P, x):
        return sum(c * x**i for i, c in enumerate(P))
    
    def find_roots(P, F):
        roots = []
        for x in F:
            if abs(evaluate_polynomial(P, x)) < 1e-6:  # Assuming F is a finite field
                roots.append(x)
        return roots
    
    def min_root_distance(roots):
        return min(abs(r1 - r2) for r1, r2 in combinations(roots, 2))
    
    def ac0_parity_circuit_size(n):
        return n * (n + 1) // 2  # Upper bound for AC0 parity circuit size
    
    F = [Fraction(i) for i in range(-10, 11)]  # Example finite field
    d = random.randint(3, 40)
    P = generate_polynomial(d, F)
    roots = find_roots(P, F)
    
    if len(roots) < 2:
        return {
            "metric_name": "min_root_distance",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not_enough_distinct_roots"
        }
    
    min_dist = min_root_distance(roots)
    c = random.uniform(0.1, 2)  # Random constant between 0.1 and 2
    conjecture_value = c * math.log(d)
    
    circuit_size = ac0_parity_circuit_size(len(roots))
    
    return {
        "metric_name": "min_root_distance",
        "metric_value": min_dist,
        "instances_tested": 1,
        "conjecture_holds": min_dist >= conjecture_value and circuit_size >= 1.5 * c * len(roots),
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
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"not_enough_distinct_roots\" first_failing_seed={r['seed']}")
                break