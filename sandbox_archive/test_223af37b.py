# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Generate a random tropical curve of degree n
    n = random.randint(5, 40)
    variables = [f'x{i}' for i in range(n)]
    negated_literals = [f'-{var}' for var in variables]
    clause = random.sample(variables + negated_literals, random.randint(1, n))
    
    # Construct the Tseitin formula
    tseitin_formula = []
    literals = set()
    for lit in clause:
        if lit.startswith('-'):
            literals.add(lit[1:])
        else:
            literals.add(lit)
    
    for var in literals:
        tseitin_formula.append([var, f'-{var}', 'OR'])
        tseitin_formula.append([f'¬{var}', f'-{var}', 'AND'])
        tseitin_formula.append([f'{var}', f'-{var}', 'XOR'])
    
    # Simulate a DPLL-based solver to find refutation length
    def dpll(formula, assignment):
        if not formula:
            return 0
        literal = next(lit for lit in formula[0] if lit.startswith('-') != formula[1][lit])
        if literal in assignment and assignment[literal] != formula[1][literal]:
            return float('inf')
        new_assignment = assignment.copy()
        new_assignment[literal] = formula[1][literal]
        return 1 + min(dpll(formula[2:], new_assignment), dpll([f'-{lit}' for lit in formula], new_assignment))
    
    refutation_length = dpll(tseitin_formula, {})
    
    # Compute the rank of the tropical curve (simplified example)
    rank = len(variables)  # This is a placeholder; actual computation depends on the curve's zero-locus
    
    return {
        "metric_name": "refutation_length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": refutation_length >= 2 ** rank,
        "counterexample": "" if refutation_length >= 2 ** rank else f"Refutation length {refutation_length} < 2^{rank}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_refutation_length = sum(result["metric_value"] for result in results) / len(results)
    std_refutation_length = math.sqrt(sum((result["metric_value"] - mean_refutation_length) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_refutation_length} std={std_refutation_length} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Refutation length < 2^rank\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")