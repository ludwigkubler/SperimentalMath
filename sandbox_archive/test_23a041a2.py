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

def generate_instance(n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(2 * n):
        clause = random.sample(variables, 3)
        clause.append(random.choice(['', 'NOT ']))
        clauses.append(clause)
    return variables, clauses

def evaluate_circuit(circuit, assignment):
    stack = []
    inputs = circuit[::-1]
    for item in inputs:
        if isinstance(item, list):
            var = item[0]
            negate = item[1] == 'NOT '
            value = assignment[var] if not negate else not assignment[var]
            stack.append(value)
        elif item == 'AND':
            a = stack.pop()
            b = stack.pop()
            stack.append(a and b)
        elif item == 'OR':
            a = stack.pop()
            b = stack.pop()
            stack.append(a or b)
    return stack[0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_hv = 0
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            variables, clauses = generate_instance(n)
            circuit = []
            for clause in clauses:
                if random.choice([True, False]):
                    circuit.append(clause)
                else:
                    circuit.extend(['NOT ' + var if negate else var for var, negate in zip(clauses, [random.choice([True, False]) for _ in range(len(clauses))])])
            
            assignment = {var: random.choice([True, False]) for var in variables}
            result = evaluate_circuit(circuit, assignment)
            instances_tested += 1
            total_hv += abs(result - n**(2/3))
        
        mean_hv = total_hv / instances_tested
        if any(abs(mean_hv - n**(2/3)) > 0.5 * n**(2/3) for n in n_values):
            return {
                "metric_name": "Hyperbolic Volume",
                "metric_value": mean_hv,
                "instances_tested": instances_tested,
                "n_max": max(n_values),
                "conjecture_holds": False,
                "counterexample": f"Mean HV {mean_hv} not within 1.5 factor of n^(2/3) for some n"
            }
    
    return {
        "metric_name": "Hyperbolic Volume",
        "metric_value": mean_hv,
        "instances_tested": instances_tested * len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"Mean HV not within 1.5 factor of n^(2/3)\" first_failing_seed={first_failing_seed}")