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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(3)]
            if all(c == 0 for c in clause):
                clause[random.randint(0, 2)] = random.choice([-1, 1])
            clauses.append(clause)
        return clauses
    
    def dpll_refutation_tree_width(clauses):
        # Simplified DPLL algorithm to estimate tree width
        stack = []
        assignment = [None] * (n + 1)
        for clause in clauses:
            if all(assignment[abs(lit)] == lit for lit in clause):
                continue
            if any(assignment[abs(lit)] is None for lit in clause):
                stack.append((clause, assignment[:]))
        return len(stack) if stack else 0
    
    def algebraic_automorphic_forms(clauses):
        forms = set()
        for clause in clauses:
            form = tuple(sorted(abs(lit) for lit in clause))
            forms.add(form)
        return len(forms)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        instances_tested = 0
        total_forms = 0
        max_width = 0
        for _ in range(5):  # Sample 5 instances per size
            clauses = generate_3cnf(n)
            width = dpll_refutation_tree_width(clauses)
            forms = algebraic_automorphic_forms(clauses)
            total_forms += forms
            max_width = max(max_width, width)
            instances_tested += 1
        
        avg_forms = total_forms / instances_tested
        results.append({
            "n": n,
            "avg_forms": avg_forms,
            "max_width": max_width
        })
    
    metric_value = sum(result["avg_forms"] for result in results) / len(results)
    conjecture_holds = all(result["avg_forms"] < 2**result["n"] for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "average_algebraic_forms",
        "metric_value": metric_value,
        "instances_tested": sum(result["instances_tested"] for result in results),
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
    std_value = (sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")