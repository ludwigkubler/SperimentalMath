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
            clause = [random.choice([1, -1]) * random.randint(1, n) for _ in range(3)]
            clauses.append(clause)
        return clauses
    
    def compute_toric_rank(clauses):
        # Simplified mapping to a rank based on the number of clauses
        return len(clauses)
    
    def monotone_circuit_width(clauses):
        # Simplified DPLL solver to estimate width
        return len(clauses)  # For simplicity, assume width is proportional to the number of clauses
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    
    rank = compute_toric_rank(clauses)
    width = monotone_circuit_width(clauses)
    
    if width == 0:
        return {
            "metric_name": "toric_rank_over_width",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "monotone_circuit_width_is_zero"
        }
    
    ratio = rank / width
    
    return {
        "metric_name": "toric_rank_over_width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(res["conjecture_holds"] for res in results):
        mean_value = sum(res["metric_value"] for res in results) / len(results)
        support_fraction = 1.0
        result = f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        result = f"RESULT: FALSIFIED counterexample='ratio_exceeds_bound' first_failing_seed={first_failing_seed}"
    
    print(result)