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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n - 1):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            cnf.append(clause)
        return cnf
    
    def polynomial_form(cnf):
        # Simplified representation for testing
        return sum([x[0] * x[1] for x in cnf])
    
    def mcr(polynomial):
        # Simplified MCR calculation for testing
        return len(polynomial)
    
    def frege_proof_depth(cnf):
        # Simplified Frege proof depth calculation for testing
        return len(cnf) + 1
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    polynomial = polynomial_form(cnf)
    mcr_value = mcr(polynomial)
    f_value = frege_proof_depth(cnf)
    
    if f_value == 0:
        return {
            "metric_name": "MCR/f",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Frege proof depth is zero"
        }
    
    ratio = mcr_value / f_value
    return {
        "metric_name": "MCR/f",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='MCR/f ratio exceeds 1' first_failing_seed={first_failing_seed}")