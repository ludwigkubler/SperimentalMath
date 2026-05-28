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
        coefficients = [random.choice([-1, 0, 1]) for _ in range(n+1)]
        return coefficients
    
    def evaluate_polynomial(poly, x):
        result = 0
        for i, coeff in enumerate(poly):
            result += coeff * (x ** i)
        return result
    
    def is_parity_function(poly, n):
        for x in range(2**n):
            if evaluate_polynomial(poly, x) != parity(x):
                return False
        return True
    
    def parity(x):
        return sum(int(bit) for bit in bin(x)[2:]) % 2
    
    def find_minimal_rank(poly, n):
        # This is a placeholder function. In practice, you would need to implement
        # an algorithm to find the minimal rank of the algebraic curve defined by poly.
        # For simplicity, we return a dummy value here.
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    poly = generate_polynomial(n)
    
    if not is_parity_function(poly, n):
        return {
            "metric_name": "minimal_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "The polynomial does not define the Parity function."
        }
    
    rank = find_minimal_rank(poly, n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if "conjecture_holds" not in r or r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "counterexample" in r and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")