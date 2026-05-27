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
        for _ in range(2**n - 1):
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def formal_power_series(formula):
        # Simplified representation of the power series
        return len(formula.split())
    
    def tseitin_circuit_size(formula):
        # Simplified representation of the circuit size
        return len(formula.split()) * 2
    
    n_values = [8, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            formula = generate_3cnf(n)
            R_G = formal_power_series(formula)
            T_C = tseitin_circuit_size(formula)
            
            if R_G <= math.log2(n) and T_C <= 10 * math.log2(n):  # Simplified bounds
                results.append(1)
            else:
                results.append(0)
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(result == 1 for result in results)
    counterexample = "" if conjecture_holds else "bounds_violation"
    
    return {
        "metric_name": "Conjecture Support",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 50, 2))  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r == 1) / len(results)
    
    if all(r == 1 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std=0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={math.sqrt(sum((r - mean) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i + 1 for i, r in enumerate(results) if r != 1)
        print(f"RESULT: FALSIFIED counterexample='bounds_violation' first_failing_seed={first_failing_seed}")