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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monomial_ideal(n):
        # Generate a random monomial ideal with n variables
        return {tuple(sorted(random.sample(range(1, n + 1), k))) for k in range(1, n + 1)}
    
    def schur_weyl_rank_ratio(I, n):
        # Compute the Schur-Weyl rank ratio ρ(I)/n^{1.5}
        if not I:
            return 0
        max_degree = max(len(i) for i in I)
        return len(I) / (n ** 1.5)
    
    def is_associated_with_permanent(I):
        # Check if the ideal is associated with the permanent of an m × m matrix
        return any(all(x <= y for x, y in zip(i, range(1, len(i) + 1))) for i in I)
    
    n = random.randint(5, 40)
    I = generate_monomial_ideal(n)
    ratio = schur_weyl_rank_ratio(I, n)
    is_permanent_associated = is_associated_with_permanent(I)
    
    if not (0.75 <= ratio <= 2):
        return {
            "metric_name": "Schur-Weyl Rank Ratio",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Ratio {ratio} out of bounds"
        }
    
    if is_permanent_associated and not (0.75 <= ratio <= 2):
        return {
            "metric_name": "Schur-Weyl Rank Ratio",
            "metric_value": ratio,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Ratio {ratio} out of bounds for permanent-associated ideal"
        }
    
    return {
        "metric_name": "Schur-Weyl Rank Ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std = (sum((r["metric_value"] - mean) ** 2 for r in results) / len(results)) ** 0.5
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Ratio out of bounds' first_failing_seed={first_failing_seed}")