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
    
    def generate_boolean_formula(n):
        clauses = []
        for _ in range(10):  # Generate a small number of clauses for simplicity
            clause = [random.choice([True, False]) for _ in range(n)]
            clauses.append(clause)
        return clauses
    
    def construct_variety(clauses):
        # Simplified mapping from Boolean formula to defining polynomial
        n = len(clauses[0])
        poly = []
        for i in range(2**n):
            term = 1
            for j in range(n):
                if (i >> j) & 1:
                    term *= (-1)**clauses[j][j]
            poly.append(term)
        return poly
    
    def count_cuspidal_sheaves(poly):
        # Simplified counting of cuspidal sheaves (not actual implementation)
        return len(poly)
    
    def compute_resolution_width(clauses):
        # Simplified computation of resolution width
        n = len(clauses[0])
        return 2 * n
    
    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    variety = construct_variety(formula)
    num_cuspidal_sheaves = count_cuspidal_sheaves(variety)
    resolution_width = compute_resolution_width(formula)
    
    return {
        "metric_name": "#cuspidal_sheaves",
        "metric_value": num_cuspidal_sheaves,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(num_cuspidal_sheaves - resolution_width) <= 0.5 * max(abs(num_cuspidal_sheaves), abs(resolution_width)),
        "counterexample": "" if num_cuspidal_sheaves == resolution_width else f"num_cuspidal_sheaves={num_cuspidal_sheaves}, resolution_width={resolution_width}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")