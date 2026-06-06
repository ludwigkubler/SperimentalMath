# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(m):
        variables = list(range(1, m + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables) if random.choice([True, False]) else -random.choice(variables) for _ in range(random.randint(1, m))]
            clauses.append(clause)
        return clauses
    
    def fca(clauses):
        concepts = set()
        for clause in clauses:
            concept = tuple(sorted(set(abs(var) for var in clause)))
            concepts.add(concept)
        return len(concepts)
    
    def resolution_width(clauses):
        stack = []
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if set(stack[i]).isdisjoint(set(stack[j])):
                        continue
                    common_vars = [var for var in stack[i] if -var in stack[j]]
                    if not common_vars:
                        continue
                    new_clause = tuple(sorted([var for var in stack[i] if var not in common_vars] + [-var for var in stack[j] if var not in common_vars]))
                    break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(stack)
            stack.append(new_clause)
    
    n_max = 0
    instances_tested = 0
    total_m = 0
    total_w = 0
    
    for m in [5, 10, 15, 20, 30, 40]:
        formula = generate_formula(m)
        n_max = max(n_max, m)
        instances_tested += 1
        m_value = fca(formula)
        w_value = resolution_width(formula)
        total_m += m_value
        total_w += w_value
    
    metric_name = "Resolution Proof Width"
    metric_value = Fraction(total_w, instances_tested) / Fraction(total_m, instances_tested)
    conjecture_holds = metric_value >= 0.9 and all(m_value <= w_value for m_value, w_value in zip([5, 10, 15, 20, 30, 40], [resolution_width(generate_formula(m)) for m in [5, 10, 15, 20, 30, 40]]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": float(metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")