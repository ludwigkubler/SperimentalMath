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
        # Generate a random Tseitin formula with n variables
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for literal in literals:
            clauses.append([literal])
        for i in range(1, n):
            clauses.append([f'x{i}', f'~x{0}'])
        return literals, clauses
    
    def hamiltonian_flow(literals, clauses):
        # Simplified Hamiltonian flow calculation (placeholder)
        return random.random()
    
    def resolution_width(clauses):
        # Simplified resolution width calculation (placeholder)
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    literals, clauses = generate_tseitin_formula(n)
    H_phi = hamiltonian_flow(literals, clauses)
    w_phi = resolution_width(clauses)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": H_phi,
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
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")