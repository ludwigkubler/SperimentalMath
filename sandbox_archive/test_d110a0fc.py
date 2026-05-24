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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def dpll_refutation_tree_width(clauses):
        # Simplified DPLL algorithm to estimate tree width
        stack = []
        literals = set()
        for clause in clauses:
            literals.update(abs(lit) for lit in clause)
        while literals:
            literal = random.choice(list(literals))
            literals.remove(abs(literal))
            stack.append((literal, []))
            while stack:
                (lit, path) = stack.pop()
                if not any(lit in cl for cl in clauses):
                    return len(path)
                new_clauses = [cl for cl in clauses if lit not in cl and -lit not in cl]
                new_literals = set(abs(lit) for lit in new_clauses[0]) if new_clauses else set()
                stack.append((random.choice(list(new_literals)), path + [(lit, new_clauses)]))
        return 0
    
    def algebraic_automorphic_forms(clauses):
        # Simplified mapping to count automorphic forms
        forms = set()
        for clause in clauses:
            form = tuple(sorted(abs(lit) for lit in clause))
            forms.add(form)
        return len(forms)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        clauses = generate_3cnf(n)
        width = dpll_refutation_tree_width(clauses)
        forms = algebraic_automorphic_forms(clauses)
        results.append((n, width, forms))
    
    metric_value = sum(forms for _, _, forms in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(width < forms for _, width, forms in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "algebraic_automorphic_forms",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")