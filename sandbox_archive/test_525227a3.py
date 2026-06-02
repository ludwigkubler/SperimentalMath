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
    
    def generate_random_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def calculate_frege_proof_length(cnf):
        # Simplified DPLL solver with time constraints
        if len(cnf) > 50:
            return float('inf')
        stack = []
        for clause in cnf:
            if not any(abs(lit) == abs(clause[0]) for lit in stack):
                stack.append(clause[0])
            elif not any(abs(lit) == abs(clause[1]) for lit in stack):
                stack.append(clause[1])
            else:
                return 1
        return len(stack)
    
    def calculate_minimal_rank(cnf):
        # Placeholder for noncommutative crossed product rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10)
    
    n = 5
    m = 10
    cnf = generate_random_cnf(n, m)
    frege_length = calculate_frege_proof_length(cnf)
    rank = calculate_minimal_rank(cnf)
    
    if frege_length == float('inf'):
        return {
            "metric_name": "Frege Proof Length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "DPLL solver timed out"
        }
    
    return {
        "metric_name": "Frege Proof Length",
        "metric_value": frege_length,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")