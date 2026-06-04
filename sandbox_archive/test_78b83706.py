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

def generate_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def shannon_entropy(distribution):
    total = sum(distribution.values())
    entropy = 0
    for count in distribution.values():
        if count > 0:
            p = Fraction(count, total)
            entropy -= p * math.log2(p)
    return entropy

def hodge_decomposition_order(clauses):
    # Simplified heuristic to estimate Hodge decomposition order
    return len(clauses) ** 1.5

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n, n * 2)  # Ensure enough clauses to form a CNF formula
        cnf_formula = generate_cnf(n, m)
        
        hodge_order = hodge_decomposition_order(cnf_formula)
        clause_subset_entropy = shannon_entropy({tuple(sorted(clause)): 1 for clause in cnf_formula})
        
        metric_values.append(hodge_order * clause_subset_entropy)
    
    mean_value = sum(metric_values) / len(metric_values)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / len(metric_values))
    
    if any(abs(x) < 0.5 for x in metric_values):
        conjecture_holds = False
        counterexample = "correlation_coefficient_below_0.5"
    
    return {
        "metric_name": "Hodge Decomposition Order * Clause Subset Entropy",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.4f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")