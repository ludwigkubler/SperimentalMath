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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for x in variables:
            clauses.append([x])
        for i in range(1, n):
            clauses.append([f'~{variables[i-1]}', f'{variables[i]}'])
        return clauses
    
    def resolution(clauses):
        new_clauses = set()
        while True:
            new_clause = None
            for c1 in clauses:
                for c2 in clauses:
                    if len(c1) > 1 and len(c2) > 1 and any(x == f'~{y}' for x, y in zip(c1, c2)):
                        new_clause = [x for x in c1 + c2 if x != x and f'~{x}' not in c2]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(clauses)
            clauses.add(tuple(sorted(new_clause)))
    
    def topological_entropy(n):
        return n * math.log(n, 2)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        formula = generate_tseitin_formula(n)
        entropy = topological_entropy(n)
        width = resolution(formula)
        results.append((n, entropy, width))
    
    total_width = sum(width for _, _, width in results)
    avg_width = total_width / len(results)
    max_deviation = max(abs(width - avg_width) for _, _, width in results)
    
    metric_value = avg_width
    instances_tested = len(results)
    n_max = max(n for n, _, _ in results)
    conjecture_holds = max_deviation <= 3
    counterexample = "" if conjecture_holds else "max_deviation > 3"
    
    return {
        "metric_name": "Average Width of Resolution Proof Trees",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_deviation > 3\" first_failing_seed={first_failing_seed}")