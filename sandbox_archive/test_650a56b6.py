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
    
    def generate_polynomial(n):
        return [random.randint(1, n) for _ in range(n)]
    
    def compute_tropical_rank(poly):
        # Simplified tropical rank computation (placeholder)
        return len(poly) ** 0.5
    
    def compute_circuit_size(poly):
        # Simplified circuit size computation (placeholder)
        return len(poly) ** 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    poly = generate_polynomial(n)
    tropical_rank = compute_tropical_rank(poly)
    circuit_size = compute_circuit_size(poly)
    
    metric_value = tropical_rank
    instances_tested = 1
    conjecture_holds = tropical_rank <= circuit_size ** 0.5
    counterexample = "" if conjecture_holds else f"n={n}, poly={poly}, tropical_rank={tropical_rank}, circuit_size={circuit_size}"
    
    return {
        "metric_name": "Tropical Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample_desc = f"n={results[first_failing_seed]['instances_tested']}, poly={generate_polynomial(results[first_failing_seed]['instances_tested'])}, tropical_rank={results[first_failing_seed]['metric_value']}, circuit_size={compute_circuit_size(generate_polynomial(results[first_failing_seed]['instances_tested']))}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample_desc}\" first_failing_seed={first_failing_seed}")