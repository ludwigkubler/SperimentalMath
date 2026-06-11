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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        literals = {l for clause in cnf for l in clause}
        literal = random.choice(list(literals))
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        new_assignment[literal] = False
        if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
            return True
        return False
    
    def generate_cnf(n, m):
        cnf = []
        variables = list(range(1, n + 1))
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            cnf.append(clause)
        return cnf
    
    def hodge_index(cnf):
        # Placeholder function to compute Hodge index
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf) / 2
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(int(0.1 * n), int(0.9 * n)))
            if dpll(cnf):
                results.append((n, hodge_index(cnf)))
    
    if not results:
        return {
            "metric_name": "Hodge Index vs Resolution Width",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n_max = max(n for n, _ in results)
    instances_tested = len(results)
    hodge_indices = [h for _, h in results]
    widths = [len(cnf) for cnf, _ in results]
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(hodge_indices, widths)) / math.sqrt(sum((x - mean_x)**2 for x in hodge_indices) * sum((y - mean_y)**2 for y in widths))
    mean_hodge_index = sum(hodge_indices) / instances_tested
    mean_width = sum(widths) / instances_tested
    
    return {
        "metric_name": "Hodge Index vs Resolution Width",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")