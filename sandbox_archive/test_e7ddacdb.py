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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def qsi(cnf):
        # Constructive mapping to quasi-symmetric space
        equivalence_classes = {}
        for clause in cnf:
            key = tuple(sorted(abs(lit) for lit in clause))
            if key not in equivalence_classes:
                equivalence_classes[key] = []
            equivalence_classes[key].append(clause)
        
        return len(equivalence_classes)
    
    def resolution_width(cnf):
        # Simplified resolution width calculation
        queue = cnf[:]
        resolved = set()
        while queue:
            clause = queue.pop(0)
            if all(lit in resolved for lit in clause):
                continue
            new_literals = []
            for other_clause in cnf:
                if any(-lit in other_clause for lit in clause):
                    new_lit = -next(lit for lit in clause if -lit not in other_clause)
                    new_literals.append(new_lit)
            if new_literals:
                queue.extend([new_clause for new_clause in cnf if any(lit in new_clause for lit in new_literals)])
                resolved.update(new_literals)
        return len(resolved)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = generate_cnf(n, m)
    qsi_value = qsi(cnf)
    width = resolution_width(cnf)
    
    return {
        "metric_name": "qsi_vs_width",
        "metric_value": qsi_value,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(qsi_value - width) <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"qsi_value - width > 1\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")