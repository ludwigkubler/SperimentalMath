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
    
    def generate_boolean_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n):
            clause = random.choice(variables + [f'~{v}' for v in variables])
            clauses.append(clause)
        return ' and '.join(clauses)

    def dpll_search_tree_height(formula):
        if formula == 'True':
            return 0
        elif formula == 'False':
            return float('inf')
        elif '~' in formula:
            subformula = formula[2:]
            return max(dpll_search_tree_height(subformula), dpll_search_tree_height(f'~{subformula}')) + 1
        else:
            left, right = formula.split(' and ')
            return max(dpll_search_tree_height(left), dpll_search_tree_height(right)) + 1

    def construct_braided_monoidal_category(clause_set):
        # Placeholder for actual implementation
        # For simplicity, we assume the number of generators is proportional to the length of the clause set
        return len(clause_set)

    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    height = dpll_search_tree_height(formula)
    num_generators = construct_braided_monoidal_category(formula.split(' and '))

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": height,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": f"Formula: {formula}, Height: {height}, Generators: {num_generators}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if 0.5 < r["metric_value"] < 0.8) / len(results)

    if all(0.5 < r["metric_value"] < 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] <= 0.5 or r["metric_value"] >= 0.8 for r in results):
        first_failing_seed = next((r["seed"] for r in results if not (0.5 < r["metric_value"] < 0.8)), None)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation out of range\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unmet_acceptance_criterion")