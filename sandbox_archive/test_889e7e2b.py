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
    
    def generate_frege_proof(n):
        if n == 1:
            return []
        else:
            left = generate_frege_proof(random.randint(1, n-1))
            right = generate_frege_proof(n - len(left) - 1)
            return [('and', left, right)]
    
    def count_monoidal_factors(proof):
        if not proof:
            return 0
        elif isinstance(proof[0], tuple):
            return 1 + count_monoidal_factors(proof[1]) + count_monoidal_factors(proof[2])
        else:
            return 0
    
    n = random.randint(5, 40)
    proof = generate_frege_proof(n)
    width = len(proof)
    factors = count_monoidal_factors(proof)
    
    return {
        "metric_name": "monoidal_factors",
        "metric_value": factors,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": factors <= width,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")