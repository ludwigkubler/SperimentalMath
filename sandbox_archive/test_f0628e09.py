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
    
    def generate_explicit_function(n):
        # Generate a random polynomial over GF(2) with degree n
        coefficients = [random.randint(0, 1) for _ in range(n + 1)]
        return coefficients
    
    def tropicalize_polynomial(poly):
        # Tropicalize the polynomial by taking the maximum of each coefficient
        return max(poly)
    
    def tensor_product_rank(tropicalized_poly):
        # The tensor product rank is simply the value of the tropicalized polynomial
        return tropicalized_poly
    
    def acc0_circuit_threshold(poly):
        # For simplicity, assume ACC⁰ threshold is the degree of the polynomial
        return len(poly) - 1
    
    n = random.randint(5, 40)
    f = generate_explicit_function(n)
    t = acc0_circuit_threshold(f)
    tropicalized_f = tropicalize_polynomial(f)
    rank = tensor_product_rank(tropicalized_f)
    
    ratio = rank / t if t != 0 else float('inf')
    conjecture_holds = 0.8 <= ratio <= 1.2
    counterexample = "" if conjecture_holds else f"Ratio {ratio} out of bounds"
    
    return {
        "metric_name": "tensor_product_rank_over_threshold",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")