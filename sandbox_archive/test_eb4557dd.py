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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not all(abs(x) == 1 for x in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def compute_automorphisms(cnf):
        n = len(cnf[0])
        auts = [1]
        for perm in permutations(range(n)):
            is_aut = True
            for clause in cnf:
                if all(perm[abs(x) - 1] * x for x in clause) != any(perm[abs(x) - 1] * x for x in clause):
                    is_aut = False
                    break
            if is_aut:
                auts.append(tuple(perm))
        return len(set(auts))
    
    def compute_clause_set_complexity(cnf):
        n = len(cnf[0])
        return sum(len(clause) for clause in cnf)
    
    def permutations(lst):
        if not lst:
            yield []
        else:
            for perm in permutations(lst[1:]):
                for i in range(len(perm) + 1):
                    yield perm[:i] + [lst[0]] + perm[i:]
    
    n_values = [5, 10, 15, 20, 30, 40]
    num_instances_per_n = 5
    total_instances = sum(num_instances_per_n for n in n_values)
    
    if total_instances > 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Too many instances per seed"
        }
    
    auts = []
    complexities = []
    for n in n_values:
        for _ in range(num_instances_per_n):
            cnf = generate_cnf(n)
            if not cnf:
                continue
            auts.append(compute_automorphisms(cnf))
            complexities.append(compute_clause_set_complexity(cnf))
    
    if len(auts) < 30 or len(complexities) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Not enough instances"
        }
    
    mean_aut = sum(auts) / len(auts)
    mean_complexity = sum(complexities) / len(complexities)
    covariance = sum((a - mean_aut) * (c - mean_complexity) for a, c in zip(auts, complexities)) / len(auts)
    variance_aut = sum((a - mean_aut) ** 2 for a in auts) / len(auts)
    variance_complexity = sum((c - mean_complexity) ** 2 for c in complexities) / len(complexities)
    
    if variance_aut == 0 or variance_complexity == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Zero variance in auts or complexities"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_aut) * math.sqrt(variance_complexity))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(auts),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")