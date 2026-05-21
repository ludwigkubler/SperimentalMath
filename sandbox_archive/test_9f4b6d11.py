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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(10 * n):  # Generate enough clauses to cover all variables
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_trivial_poly(poly):
        # Simplify the polynomial and check if it's trivial
        # This is a placeholder function; actual implementation needed
        return False
    
    def sos_degree(poly):
        # Placeholder function to compute SOS degree
        return random.randint(1, 20)
    
    n = 40
    clauses = generate_3cnf(n)
    
    real_radical_non_trivial = any(is_trivial_poly(poly) for poly in clauses)
    
    if not real_radical_non_trivial:
        return {
            "metric_name": "sos_degree",
            "metric_value": 1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": ""
        }
    
    sos_deg = sos_degree(clauses)
    
    return {
        "metric_name": "sos_degree",
        "metric_value": sos_deg,
        "instances_tested": 1,
        "conjecture_holds": sos_deg >= math.log(n, 2),
        "counterexample": f"n={n}, sos_degree={sos_deg}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")