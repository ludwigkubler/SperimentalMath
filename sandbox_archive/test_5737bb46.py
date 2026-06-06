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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def is_satisfiable(model):
            for clause in cnf:
                if not any(lit in model and (model[lit] == 1) or (-lit in model and (model[-lit] == -1)) for lit in clause):
                    return False
            return True
        
        def backtrack(model, literals):
            if is_satisfiable(model):
                return model
            if not literals:
                return None
            literal = literals[0]
            model[literal] = 1
            result = backtrack(model, literals[1:])
            if result:
                return result
            del model[literal]
            model[-literal] = -1
            result = backtrack(model, literals[1:])
            if result:
                return result
            del model[-literal]
            return None
        
        return backtrack({}, list(range(1, len(cnf) + 1)))
    
    def arithmetic_hierarchy_depth(cnf):
        depth = 0
        for clause in cnf:
            for lit in clause:
                depth = max(depth, abs(lit))
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        path_length = len(dpll(cnf)) if dpll(cnf) else float('inf')
        depth = arithmetic_hierarchy_depth(cnf)
        results.append((n, depth, path_length))
    
    correlation_coefficient = 0
    for i in range(len(n_values)):
        for j in range(i + 1, len(n_values)):
            n1, d1, p1 = results[i]
            n2, d2, p2 = results[j]
            if (n1 != n2) and (d1 != d2) and (p1 != p2):
                correlation_coefficient += ((d1 - d2) * (p1 - p2)) / math.sqrt((d1**2 + d2**2) * (p1**2 + p2**2))
    
    correlation_coefficient /= len(results)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else "Correlation Coefficient < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation Coefficient < 0.8\" first_failing_seed={first_failing_seed}")