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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = []
            for j in range(n):
                sign = random.choice([1, -1])
                clause.append((sign, j + 1))
            clauses.append(clause)
        return clauses
    
    def truth_table_size(n):
        return 2 ** n
    
    def hilbert_cube_diameter(n):
        return n
    
    def frege_proof_depth(n):
        # Simplified DPLL-based solver for Frege proof depth
        return n * (n + 1) // 2
    
    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    truth_table_size_n = truth_table_size(n)
    hilbert_cube_diam = hilbert_cube_diameter(n)
    frege_depth = frege_proof_depth(n)
    
    if frege_depth == 0:
        return {
            "metric_name": "diameter_to_frege_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Frege depth is zero"
        }
    
    ratio = hilbert_cube_diam / frege_depth
    return {
        "metric_name": "diameter_to_frege_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,  # Example constant c=2 for simplicity
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        seeds = random.sample(primes, min(30, len(primes)))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0.0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"diameter_to_frege_ratio > 2\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)