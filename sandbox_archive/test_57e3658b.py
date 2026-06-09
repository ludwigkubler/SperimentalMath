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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10 * n):  # Generate 10 clauses per variable
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def solve(model):
            if not cnf:
                return True
            literals = set()
            for clause in cnf:
                literals.update(clause)
            pure_literal = next((l for l in literals if (all(l in model or -l in model for m in cnf)) and not any(-l in m or l in m for m in cnf)), None)
            if pure_literal is None:
                return False
            new_model = model.copy()
            new_model[pure_literal] = True
            if solve(new_model):
                return True
            new_model[pure_literal] = False
            if solve(new_model):
                return True
            return False
        
        n = len(cnf[0])
        return solve({})
    
    def deligne_lusztig_representation(cnf):
        # Placeholder for Deligne-Lusztig representation calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 10 * len(cnf))
    
    n = 20  # Fixed size for simplicity
    cnf = generate_cnf(n)
    m_phi = deligne_lusztig_representation(cnf)
    d_phi = len(dpll(cnf))  # Frege proof depth
    
    if d_phi == 0:
        return {
            "metric_name": "m(φ)/d(φ)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Frege proof depth is zero"
        }
    
    ratio = Fraction(m_phi, d_phi)
    return {
        "metric_name": "m(φ)/d(φ)",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(ratio - 1) <= Fraction(1, 10),
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 8)]  # Default list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")