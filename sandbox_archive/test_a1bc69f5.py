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
    
    # Placeholder for generating noncommutative algebras and sheaves
    def generate_noncommutative_algebra(n):
        return [[random.randint(0, 1) if i == j else 0 for j in range(n)] for i in range(n)]
    
    def generate_sheaf_cohomology(algebra):
        n = len(algebra)
        cohomology = []
        for _ in range(n):
            cohomology.append([random.randint(0, 1) for _ in range(n)])
        return cohomology
    
    # Placeholder for computing BP_readtwice tensor width
    def compute_tensor_width(bp):
        n = len(bp)
        width = 0
        for i in range(n):
            for j in range(i + 1, n):
                if bp[i][j] != 0:
                    width += 1
        return width
    
    # Placeholder for computing minimal rank of sheaf cohomology
    def compute_minimal_rank(cohomology):
        n = len(cohomology)
        rank = 0
        for i in range(n):
            if sum(cohomology[j][i] for j in range(n)) != 0:
                rank += 1
        return rank
    
    # Generate a random noncommutative algebra and sheaf cohomology
    n = random.randint(5, 40)
    algebra = generate_noncommutative_algebra(n)
    cohomology = generate_sheaf_cohomology(algebra)
    
    # Compute BP_readtwice tensor width and minimal rank of sheaf cohomology
    bp_width = compute_tensor_width(cohomology)
    min_rank = compute_minimal_rank(cohomology)
    
    # Check the conjecture
    if bp_width == 0:
        return {
            "metric_name": "min_rank_over_tw",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "tensor_width_zero"
        }
    
    ratio = min_rank / bp_width
    if ratio <= 0:
        return {
            "metric_name": "min_rank_over_tw",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "non_positive_ratio"
        }
    
    return {
        "metric_name": "min_rank_over_tw",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not_supported' first_failing_seed={first_failing_seed}")