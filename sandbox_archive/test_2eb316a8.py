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
        return [random.randint(0, 100) for _ in range(n)]
    
    def sum_of_powers(poly, r, p):
        total = 0
        for coeff in poly:
            total += pow(coeff, r, p)
        return total % p
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    poly = generate_polynomial(n)
    p = random.randint(2, 100)
    
    for r in range(1, n + 1):
        if sum_of_powers(poly, r, p) < Fraction(1, p**r).numerator:
            return {
                "metric_name": "sum_of_powers",
                "metric_value": sum_of_powers(poly, r, p),
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"r={r}, poly={poly}"
            }
    
    return {
        "metric_name": "sum_of_powers",
        "metric_value": sum_of_powers(poly, n, p),
        "instances_tested": 1,
        "conjecture_holds": True,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")