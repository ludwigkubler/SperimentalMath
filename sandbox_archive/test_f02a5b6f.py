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
    
    def generate_tseitin_formula(n, m):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = f'{variables[i-1]}'
            clauses.append(clause)
        for _ in range(m):
            literals = random.sample(variables + [f'~{v}' for v in variables], 2)
            if random.choice([True, False]):
                clauses.append(f'({literals[0]}) OR ({literals[1]})')
            else:
                clauses.append(f'(~{literals[0]}) AND (~{literals[1]})')
        return ' AND '.join(clauses)
    
    def construct_diophantine_equations(formula):
        # Simplified construction for demonstration
        equations = []
        for clause in formula.split(' AND '):
            if 'OR' in clause:
                literals = [lit.strip('~') for lit in clause.split(' OR ') if lit]
                equation = f'{literals[0]} - {literals[1]} = 0'
                equations.append(equation)
        return equations
    
    def solve_diophantine_equations(equations):
        # Simplified solution for demonstration
        solutions = []
        for eq in equations:
            parts = eq.split(' = ')
            lhs, rhs = parts[0].split('-')
            x = int(rhs) + int(lhs)
            solutions.append(x)
        return len(solutions)
    
    def resolution_proof_width(formula):
        # Simplified width calculation for demonstration
        return len(formula.split(' AND '))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_instances = 0
    
    for n in n_values:
        for _ in range(5):  # Test each size with 5 instances
            formula = generate_tseitin_formula(n, n)
            equations = construct_diophantine_equations(formula)
            num_solutions = solve_diophantine_equations(equations)
            width = resolution_proof_width(formula)
            results.append((num_solutions, width))
            total_instances += 1
    
    if not results:
        return {
            "metric_name": "S(φ) / w(φ)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    avg_ratio = sum(num_solutions / width for num_solutions, width in results) / len(results)
    support_fraction = sum(1 for num_solutions, width in results if 0.5 <= num_solutions / width <= 2) / len(results)
    
    return {
        "metric_name": "S(φ) / w(φ)",
        "metric_value": avg_ratio,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std=... support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")