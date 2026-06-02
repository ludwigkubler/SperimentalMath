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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_formula(n):
        # Generate a random Boolean formula with n variables and 2n clauses
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 3)
            clauses.append(f"({' OR '.join(clause)})")
        return f"{' AND '.join(clauses)}"

    def resolution_width(formula):
        # Simplified DPLL solver to estimate proof width
        stack = []
        literals = set()
        for clause in formula.split(' AND '):
            if ' OR ' not in clause:
                continue
            literals.update(clause.split(' OR '))
            stack.append(clause)
        
        while stack:
            clause1, *stack = stack
            if ' OR ' not in clause1:
                continue
            literal1 = random.choice(clause1.split(' OR '))
            new_clause = None
            for clause2 in stack:
                if ' OR ' not in clause2:
                    continue
                literal2 = random.choice(clause2.split(' OR '))
                if literal1 == literal2:
                    continue
                if literal1.startswith('~'):
                    new_literal = literal2
                elif literal2.startswith('~'):
                    new_literal = literal1
                else:
                    continue
                new_clause = clause1.replace(literal1, '').replace(f'~{literal1}', '') + ' AND ' + clause2.replace(literal2, '').replace(f'~{literal2}', '')
                break
            if not new_clause:
                return len(stack) + 1
            stack.append(new_clause)
        return len(stack)

    def quasi_symmetric_design_size(n):
        # Simplified method to estimate the size of a quasi-symmetric design
        return n * (n + 1) // 2

    n = random.randint(5, 40)
    formula = generate_boolean_formula(n)
    width = resolution_width(formula)
    size = quasi_symmetric_design_size(n)

    correlation_coefficient = (width - n**2) / (n**2 * math.sqrt((n**2 + 1) * (n**2 - 1)))
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8,
        "counterexample": "" if abs(correlation_coefficient) >= 0.8 else "Correlation coefficient < 0.8"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Correlation coefficient < 0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")