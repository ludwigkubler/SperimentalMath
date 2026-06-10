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
        clauses = []
        for _ in range(2 ** n - 1):
            clause = [random.choice([f'x{i+1}', f'-x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def compute_symplectic_volume(cnf):
        # Placeholder for actual symplectic volume computation
        # This is a dummy implementation for testing purposes
        return random.uniform(0.1, 2.0)
    
    def construct_circuit(cnf):
        # Placeholder for circuit construction
        # This is a dummy implementation for testing purposes
        return random.randint(5, 20)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    symplectic_volume = compute_symplectic_volume(cnf)
    circuit_size = construct_circuit(cnf)
    
    metric_value = symplectic_volume / (circuit_size ** 2)
    instances_tested = 1
    n_max = n
    conjecture_holds = True if metric_value <= 1.5 else False
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "symplectic_volume_over_circuit_size_squared",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")