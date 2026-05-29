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

def generate_boolean_function(n, m):
    variables = list(range(1, n + 1))
    clauses = set()
    for _ in range(m):
        literals = [random.choice([1, -1]) * random.choice(variables) for _ in range(random.randint(1, n))]
        clauses.add(tuple(sorted(literals)))
    return variables, clauses

def characteristic_polynomial(clauses, variables):
    n = len(variables)
    poly = [[0] * (n + 1) for _ in range(n + 1)]
    poly[0][0] = 1
    for clause in clauses:
        product = 1
        for literal in clause:
            if literal > 0:
                product *= variables[literal - 1]
            else:
                product *= (1 - variables[-literal])
        for i in range(n, -1, -1):
            poly[i][0] += product
            for j in range(i):
                poly[j][i + 1] = poly[j + 1][i]

    # Convert to integer coefficients modulo a large prime
    prime = 2**64 - 59
    for i in range(n + 1):
        for j in range(n + 1):
            poly[i][j] %= prime

    return poly

def resolution_width(clauses, variables):
    n = len(variables)
    clauses_list = list(clauses)
    stack = []
    while clauses_list:
        clause = clauses_list.pop()
        if all(lit in variables for lit in clause):
            return len(stack) + 1
        literal = next((lit for lit in clause if -lit in variables), None)
        if literal is not None:
            stack.append(literal)
            new_clauses = set()
            for other_clause in clauses_list:
                if literal in other_clause and -literal in other_clause:
                    continue
                new_clauses.add(tuple(sorted(other_clause + (other_clause.index(-literal) + 1,))))
            clauses_list = new_clauses
        else:
            return float('inf')
    return len(stack)

def quantum_phase(poly):
    leading_coefficient = poly[0][0]
    order_of_field = 2**64 - 59
    return abs(leading_coefficient) % order_of_field

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        variables, clauses = generate_boolean_function(n, 2**n)
        poly = characteristic_polynomial(clauses, variables)
        w_f = resolution_width(clauses, variables)
        if w_f == float('inf'):
            continue
        phi_f = quantum_phase(poly)
        c_log_w_f = 10 * math.log(w_f)  # Example constant c=10 for simplicity
        results.append({"n": n, "phi_f": phi_f, "c_log_w_f": c_log_w_f})
    
    if not results:
        return {
            "metric_name": "quantum_phase_bound",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "no_valid_instances"
        }
    
    phi_f_values = [result["phi_f"] for result in results]
    c_log_w_f_values = [result["c_log_w_f"] for result in results]
    
    mean_phi_f = sum(phi_f_values) / len(phi_f_values)
    std_phi_f = math.sqrt(sum((x - mean_phi_f) ** 2 for x in phi_f_values) / len(phi_f_values))
    
    correlation_coefficient = sum((phi_f_values[i] - mean_phi_f) * (c_log_w_f_values[i] - mean_c_log_w_f) for i in range(len(results))) / (len(results) * std_phi_f * std_c_log_w_f)
    
    return {
        "metric_name": "quantum_phase_bound",
        "metric_value": correlation_coefficient,
        "instances_tested": len(phi_f_values),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": abs(correlation_coefficient) > 0.95,  # Example threshold
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(2, 32)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first_failing_seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_valid_instances")