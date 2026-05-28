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
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) * (-1 if random.choice([True, False]) else 1)]
            while len(clause) < 3:
                var = random.choice(variables)
                if var not in clause:
                    clause.append(var * (-1 if random.choice([True, False]) else 1))
            clauses.append(clause)
        return clauses
    
    def compute_grothendieck_witt_class(cnf):
        # Placeholder for Grothendieck-Witt class computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) ** 0.5
    
    def dpll_solver(cnf):
        # Placeholder for DPLL solver
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf)
    
    n = random.randint(5, 40)
    m = random.randint(n, n * 3)
    cnf = generate_cnf(n, m)
    grothendieck_witt_class = compute_grothendieck_witt_class(cnf)
    refutation_size = dpll_solver(cnf)
    
    return {
        "metric_name": "Gen(F,p)",
        "metric_value": grothendieck_witt_class,
        "instances_tested": 1,
        "conjecture_holds": grothendieck_witt_class >= refutation_size,
        "counterexample": "" if grothendieck_witt_class >= refutation_size else "Gen(F,p) < refutation size"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len(results) / len(seeds)
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Gen(F,p) < refutation size\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")