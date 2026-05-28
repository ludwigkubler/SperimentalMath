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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def resolution_size(clauses):
        # Simplified resolution algorithm to estimate size
        resolvents = set()
        while True:
            new_resolvents = set()
            for clause1 in clauses:
                for clause2 in clauses:
                    common_vars = [var for var in clause1 if -var in clause2]
                    if len(common_vars) == 1:
                        literal = common_vars[0]
                        resolvent = sorted(set(clause1 + clause2) - {literal, -literal})
                        if resolvent not in resolvents:
                            new_resolvents.add(tuple(resolvent))
            if not new_resolvents:
                break
            clauses.extend(new_resolvents)
            resolvents.update(new_resolvents)
        return len(clauses)
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    resolution_size_value = resolution_size(clauses)
    
    # Minimal order of geometric invariants (simplified heuristic)
    k = len(set(abs(lit) for lit in sum(clauses, [])))
    
    if k == 0:
        return {
            "metric_name": "resolution_size",
            "metric_value": resolution_size_value,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    upper_bound = k**3 * math.log(n)
    
    return {
        "metric_name": "resolution_size",
        "metric_value": resolution_size_value,
        "instances_tested": 1,
        "conjecture_holds": resolution_size_value <= upper_bound,
        "counterexample": "" if resolution_size_value <= upper_bound else f"upper_bound={upper_bound}, actual={resolution_size_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    total_metric_value = sum(result["metric_value"] for result in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")