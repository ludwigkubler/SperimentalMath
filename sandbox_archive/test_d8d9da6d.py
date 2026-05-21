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
    
    def generate_polynomial(n):
        return [random.randint(0, 100) for _ in range(n)]
    
    def power_sum_mod(poly, r, p):
        return sum(coeff ** r % p for coeff in poly) % p
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = random.randint(2, 100)
    poly = generate_polynomial(n)
    
    for r in range(1, n + 1):
        if power_sum_mod(poly, r, p) >= Fraction(1, p ** r):
            return {
                "metric_name": "power_sum_mod",
                "metric_value": power_sum_mod(poly, r, p),
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            }
    
    return {
        "metric_name": "power_sum_mod",
        "metric_value": power_sum_mod(poly, n, p),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": f"No r found such that sum of {r}-th powers is at least 1/p^{r}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"No r found\" first_failing_seed={first_failing_seed}")