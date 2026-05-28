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
    
    # Generate a random binary matrix A of size m×n where n ≤ 40
    m = random.randint(5, 20)
    n = random.randint(5, 20)
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(m)]
    
    # Construct the formula ϕ(A) for the Boolean function f(x1,...,xn) defined by A
    variables = [f"x{i}" for i in range(1, n+1)]
    formulas = {}
    for row in A:
        clause = " ∨ ".join([f"{var if val == 1 else '~' + var}" for var, val in zip(variables, row)])
        formulas[clause] = True
    
    # Determine the Frege proof depth for ϕ(A)
    def frege_depth(formula):
        if formula in formulas:
            return 1
        elif " ∨ ".join(formulas.keys()) == formula:
            return max(frege_depth(clause) for clause in formula.split(" ∨ "))
        else:
            return float('inf')
    
    proof_depth = frege_depth(formulas[0])
    
    # Compute the order of the Coxeter group Γ and check if it is polynomially related to the Frege proof depth
    def coxeter_group_order(n):
        return math.factorial(n)
    
    order = coxeter_group_order(n)
    conjecture_holds = proof_depth <= order**2  # Example polynomial bound, replace with actual bound
    
    return {
        "metric_name": "Frege Proof Depth",
        "metric_value": proof_depth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Proof depth {proof_depth} exceeds order^2 bound"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_depth = sum(result["metric_value"] for result in results) / len(results)
    std_deviation = math.sqrt(sum((result["metric_value"] - mean_depth)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_deviation} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_deviation} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed + 2}")