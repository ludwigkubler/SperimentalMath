# auto-injected by SEC sandbox
import math
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
from itertools import product

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        literals = [f"p{i}" if i % 2 == 0 else f"~p{i}" for i in range(1, n+1)]
        clause = random.choice(literals)
        for _ in range(random.randint(1, n-1)):
            clause += " & " + random.choice(literals)
        clauses.append("(" + clause + ")")
    return " | ".join(clauses)

def evaluate_cnf(cnf, assignment):
    return eval(cnf.replace("p", str(assignment)).replace("~p", str(not assignment)))

def compute_entropy(probabilities):
    entropy = 0
    for p in probabilities:
        if p > 0:
            entropy -= p * math.log2(p)
    return entropy

def dpll_width(cnf, n):
    def backtrack(assignment):
        if all(evaluate_cnf(cnf, assignment) for c in cnf.split(" | ")):
            return len(max(assignment.keys(), key=lambda k: assignment[k]))
        if any(not evaluate_cnf(cnf, assignment) for c in cnf.split(" | ")):
            return 0
        var = next(k for k in range(n) if k not in assignment)
        assignment[var] = True
        width1 = backtrack(assignment)
        del assignment[var]
        assignment[var] = False
        width2 = backtrack(assignment)
        del assignment[var]
        return max(width1, width2)
    return backtrack({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        assignments = list(product([True, False], repeat=n))
        probabilities = [Fraction(sum(1 for assignment in assignments if evaluate_cnf(cnf, assignment)), len(assignments)) for _ in range(2**n)]
        entropy = compute_entropy(probabilities)
        width = dpll_width(cnf, n)
        results.append({"n": n, "entropy": entropy, "width": width})
    
    correlation_coefficient = 0
    n_max = max(result["n"] for result in results)
    instances_tested = len(results) * len(n_values)
    
    if n_max < 16:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": correlation_coefficient,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "n_max < 16"
        }
    
    for i in range(1, len(results)):
        correlation_coefficient += (results[i]["entropy"] - results[0]["entropy"]) * (results[i]["width"] - results[0]["width"])
    
    correlation_coefficient /= (len(results) - 1) * sum((result["width"] - results[0]["width"])**2 for result in results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(1, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")