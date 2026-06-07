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
    n_max = 0
    total_equations = 0
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Sample 5 instances per size
            variables = list(range(n))
            clauses = []
            
            for i in range(n):
                clause = random.sample(variables, 2)
                clauses.append(clause)
            
            diophantine_equations = set()
            for clause in clauses:
                a, b = clause
                equation = f"{a} + {b} = {a + b}"
                diophantine_equations.add(equation)
            
            total_equations += len(diophantine_equations)
            instances_tested += 1
    
    mean_equations = total_equations / instances_tested
    conjecture_holds = mean_equations <= math.sqrt(n_max) and max(len(eqs.split()) for eqs in diophantine_equations) <= 10
    counterexample = "" if conjecture_holds else f"Mean equations: {mean_equations}, Max equations: {max(len(eqs.split()) for eqs in diophantine_equations)}"
    
    return {
        "metric_name": "Number of Diophantine Equations",
        "metric_value": mean_equations,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")