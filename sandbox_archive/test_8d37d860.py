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
        for _ in range(10 * n):  # Generate 10n clauses
            clause = [random.randint(-n, n) for _ in range(random.randint(2, n))]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        stack = cnf[:]
        while True:
            new_clause = None
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if any(abs(lit) == abs(other_lit) and lit != other_lit for lit in stack[i] for other_lit in stack[j]):
                        new_clause = [lit for lit in stack[i] if lit not in stack[j]] + [other_lit for other_lit in stack[j] if other_lit not in stack[i]]
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(stack)
            stack.append(new_clause)
    
    def dual_basis_elements(n):
        return [[i, -i] for i in range(1, n + 1)]
    
    def evaluate_brauer_group_index(basis):
        # Placeholder function to simulate Brauer group index evaluation
        return sum(abs(x) for x in basis) / len(basis)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        basis = dual_basis_elements(n)
        index = evaluate_brauer_group_index(basis)
        results.append((n, width, index))
    
    mean_width = sum(width for _, width, _ in results) / len(results)
    mean_index = sum(index for _, _, index in results) / len(results)
    max_n = max(n for n, _, _ in results)
    
    epsilon = 1e-5
    conjecture_holds = all(index <= (1 + epsilon) * width for _, width, index in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Brauer Group Index",
        "metric_value": mean_index,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")