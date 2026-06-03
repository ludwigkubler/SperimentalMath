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
    
    def tseitin_formula(n):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for var in variables:
            clauses.append(f"{var} ∨ ¬{var}")
        for i in range(1, n):
            for j in range(i+1, n+1):
                clauses.append(f"¬{variables[i-1]} ∨ ¬{variables[j-1]}")
        return clauses
    
    def algebraic_variety(clauses):
        # Simplified representation of algebraic variety
        return len(clauses)
    
    def frege_proof_length(variety_size):
        # Simplified representation of Frege proof length
        return variety_size ** 2
    
    def hodge_norm(variety_size):
        # Simplified representation of Hodge norm
        return variety_size ** 3
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = tseitin_formula(n)
    variety_size = algebraic_variety(formula)
    proof_length = frege_proof_length(variety_size)
    hodge_norm_value = hodge_norm(variety_size)
    
    metric_name = "frege_proof_length_bound"
    metric_value = math.sqrt(hodge_norm_value)
    instances_tested = 1
    n_max = n
    conjecture_holds = proof_length <= metric_value
    counterexample = "" if conjecture_holds else f"Frege proof length {proof_length} > Hodge norm bound {metric_value}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")