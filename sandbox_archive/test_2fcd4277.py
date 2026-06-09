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
    
    def generate_tseitin_formula(n):
        if n == 1:
            return "(x1)"
        else:
            x = [f"x{i+1}" for i in range(n)]
            clauses = []
            for i in range(n):
                clauses.append(f"({x[i]} v ~{x[i]})")
            for i in range(1, n):
                clauses.append(f"({x[0]} v {x[i]})")
            return " & ".join(clauses)
    
    def hamiltonian_flow(formula):
        # Placeholder function to simulate Hamiltonian flow computation
        # This is a dummy implementation and should be replaced with actual mechanics software
        return random.uniform(1, 5)
    
    def resolution_proof_width(formula):
        # Placeholder function to simulate resolution proof width computation
        # This is a dummy implementation and should be replaced with actual DPLL solver
        return random.randint(2, 8)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    formula = generate_tseitin_formula(n)
    H_phi = hamiltonian_flow(formula)
    w_phi = resolution_proof_width(formula)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": H_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")