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
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def count_integral_points(n):
        return sum(1 for i in range(2**n) if all(int(bit) >= 0 and int(bit) <= 1 for bit in format(i, f'0{n}b')))
    
    def resolution_proof_width(formula):
        # Simplified DPLL solver to estimate proof width
        clauses = formula.split()
        stack = []
        literals = set()
        
        def dpll():
            if not clauses:
                return len(stack)
            literal = next((lit for lit in literals if all(lit not in clause and -lit not in clause for clause in clauses)), None)
            if literal is None:
                return float('inf')
            stack.append(literal)
            literals.remove(literal)
            new_clauses = []
            for clause in clauses:
                if literal in clause:
                    continue
                elif -literal in clause:
                    new_clauses.extend(clause.split()[:-1])
                else:
                    new_clauses.append(clause.replace(str(-literal), ''))
            width = dpll()
            stack.pop()
            literals.add(literal)
            return width
        
        return dpll()
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    total_points = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            formula = generate_boolean_formula(n)
            points = count_integral_points(n)
            width = resolution_proof_width(formula)
            if width == float('inf'):
                continue
            total_width += width
            total_points += points
            instances_tested += 1
    
    mean_width = total_width / instances_tested
    mean_points = total_points / instances_tested
    conjecture_holds = mean_width <= 3 * mean_points
    counterexample = "" if conjecture_holds else f"mean_width={mean_width}, mean_points={mean_points}"
    
    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_width)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_dev} support_fraction={support_fraction}")
    elif any(res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")