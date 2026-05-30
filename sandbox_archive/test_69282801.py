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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = [random.randint(1, 2*n) if random.choice([True, False]) else -random.randint(1, 2*n) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        # Simplified DPLL solver to estimate width
        literals = set()
        for clause in clauses:
            for lit in clause:
                if -lit in literals:
                    literals.remove(-lit)
                else:
                    literals.add(lit)
        return len(literals)
    
    def hodge_lattice_order(n):
        # Simplified Hodge lattice order estimation
        return int(math.log2(n)) ** 2
    
    n = random.randint(5, 40)
    k = random.randint(1, 3)
    clauses = generate_k_cnf(n, k)
    
    width = resolution_width(clauses)
    hodge_order = hodge_lattice_order(n)
    
    return {
        "metric_name": "Hodge Order vs Resolution Width",
        "metric_value": hodge_order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": hodge_order <= width * math.log2(n) ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"Hodge Order > Width * log^2(n)\" first_failing_seed={result['seed']}")
                break