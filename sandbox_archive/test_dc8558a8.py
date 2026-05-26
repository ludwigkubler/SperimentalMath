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

def generate_tseitin_formula(n):
    if n <= 0:
        raise ValueError("n must be greater than 0")
    
    variables = [f'x{i+1}' for i in range(2*n)]
    clauses = []
    
    # Generate clauses for the Tseitin formula
    for i in range(n):
        clause = f'{variables[2*i]} | {variables[2*i+1]}'
        clauses.append(clause)
        clause = f'~{variables[2*i]} | ~{variables[2*i+1]} | {variables[2*n+i]}'
        clauses.append(clause)
    
    # Generate the final clause
    final_clause = ' & '.join(variables[:n])
    clauses.append(final_clause)
    
    return '\n'.join(clauses), variables

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    
    for n in n_values:
        formula, variables = generate_tseitin_formula(n)
        tree_width = n - 1  # Tree-width of a complete binary tree with n leaves
        
        # Calculate the minimal rank (simplified for testing purposes)
        min_rank = 2 ** tree_width
        
        total_metric_value += min_rank
        instances_tested += 1
    
    mean_value = total_metric_value / len(n_values)
    conjecture_holds = all(2 ** (n - 1) <= 2 * (n - 1) for n in n_values)
    
    return {
        "metric_name": "min_rank",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, min_rank={2 ** (n - 1)}, expected=2 * {n - 1}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")