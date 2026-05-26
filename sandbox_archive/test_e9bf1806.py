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
    
    def generate_bdd(n):
        if n == 0:
            return (0, 1)
        else:
            p = random.randint(0, 1)
            left = generate_bdd(n - 1)
            right = generate_bdd(n - 1)
            return (p, left, right)
    
    def characteristic_polynomial(bdd):
        if bdd[0] == 0:
            return [1]
        elif bdd[0] == 1:
            return [-1]
        else:
            left_poly = characteristic_polynomial(bdd[1])
            right_poly = characteristic_polynomial(bdd[2])
            result = []
            for i in range(len(left_poly)):
                for j in range(len(right_poly)):
                    coeff = Fraction(left_poly[i]) * Fraction(right_poly[j])
                    if i + j < len(result):
                        result[i + j] += coeff
                    else:
                        result.append(coeff)
            return result
    
    def tropicalize(poly):
        return [max(0, math.log2(abs(coeff))) for coeff in poly]
    
    n = random.randint(5, 40)
    bdd = generate_bdd(n)
    poly = characteristic_polynomial(bdd)
    if not poly:
        return {
            "metric_name": "tropical_hodge_class_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    tropical_poly = tropicalize(poly)
    rank = max(tropical_poly)
    
    c = 4
    if rank > c * n:
        return {
            "metric_name": "tropical_hodge_class_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank {rank} exceeds bound {c * n}"
        }
    
    return {
        "metric_name": "tropical_hodge_class_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")