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

def generate_unsat_3cnf(n):
    clauses = []
    for _ in range(2 * n):
        literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
        if sum(literals) != 0:
            clauses.append(tuple(sorted(literals)))
    return clauses

def evaluate_polynomial(poly, assignment):
    result = 1
    for clause in poly:
        product = 1
        for literal in clause:
            var = abs(literal)
            sign = -1 if literal < 0 else 1
            if assignment[var] == 0:
                product *= (1 - sign)
            elif assignment[var] == 1:
                product *= sign
            else:
                raise ValueError("Invalid assignment value")
        result += product
    return result % 2

def frobenius_trace_defect(poly, n):
    d_3 = 0
    for a in range(3**n):
        assignment = [(a // (3**(i-1))) % 3 for i in range(1, n+1)]
        if evaluate_polynomial(poly, assignment) ** 3 != evaluate_polynomial(poly, assignment):
            d_3 += 1
    return d_3

def build_circuit(n, depth):
    if depth == 0:
        return [random.choice([0, 1])]
    inputs = build_circuit(n, depth - 1)
    gate = random.choice(['AND', 'OR', 'NOT'])
    if gate == 'NOT':
        return [gate + '(' + str(inputs[0]) + ')']
    else:
        return [gate + '(' + str(inputs[0]) + ', ' + str(inputs[1]) + ')']

def evaluate_circuit(circuit, assignment):
    stack = []
    for token in circuit:
        if token.startswith('AND') or token.startswith('OR'):
            op2 = stack.pop()
            op1 = stack.pop()
            if token.startswith('AND'):
                result = 1 if int(op1) == 1 and int(op2) == 1 else 0
            else:
                result = 1 if int(op1) == 1 or int(op2) == 1 else 0
        elif token.startswith('NOT'):
            op = stack.pop()
            result = 1 - int(op)
        else:
            result = assignment[int(token)]
        stack.append(result)
    return stack[0]

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 10, 12]
    results = []
    
    for n in n_values:
        unsat_3cnf = generate_unsat_3cnf(n)
        poly = defaultdict(int)
        for clause in unsat_3cnf:
            poly[clause] += 1
        
        d_3 = frobenius_trace_defect(poly, n)
        
        max_depth = int(0.5 * n) + 2
        best_size = float('inf')
        for depth in range(max_depth):
            circuit = build_circuit(n, depth)
            if evaluate_circuit(circuit, [random.choice([0, 1]) for _ in range(n)]) == 1:
                size = sum(1 for token in circuit if isinstance(token, str))
                if size < best_size:
                    best_size = size
        
        S_hat_F = 2 ** (best_size - 1)
        
        slack = math.log2(S_hat_F) - (0.25 * d_3 / 3**(n/2))
        results.append({
            "metric_name": "slack",
            "metric_value": slack,
            "instances_tested": 1,
            "conjecture_holds": slack >= 0,
            "counterexample": ""
        })
    
    mean_slack = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    return {
        "seed": seed,
        "mean_slack": mean_slack,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")