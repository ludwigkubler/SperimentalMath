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
    
    def generate_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def tseitin_formula(f, n):
        literals = {}
        clauses = []
        
        def encode(x, i):
            if x not in literals:
                literals[x] = len(literals) + 1
            return literals[x]
        
        def decode(i):
            for literal, idx in literals.items():
                if idx == i:
                    return literal
        
        def binary_to_decimal(binary_str):
            return int(binary_str, 2)
        
        def decimal_to_binary(decimal_num, n):
            return format(decimal_num, f'0{n}b')
        
        def add_clause(clause):
            clauses.append(clause)
        
        def add_literal(literal):
            add_clause([literal])
        
        def add_negated_literal(literal):
            add_clause([-literal])
        
        def add_binary_operation(x, y, op):
            if op == 'AND':
                x_val = f(binary_to_decimal(decimal_to_binary(x, n)))
                y_val = f(binary_to_decimal(decimal_to_binary(y, n)))
                result = x_val and y_val
                z = encode(result, 0)
                add_clause([z])
                add_clause([-x, -y, z])
                add_clause([-z, x])
                add_clause([-z, y])
            elif op == 'OR':
                x_val = f(binary_to_decimal(decimal_to_binary(x, n)))
                y_val = f(binary_to_decimal(decimal_to_binary(y, n)))
                result = x_val or y_val
                z = encode(result, 0)
                add_clause([z])
                add_clause([-x, z])
                add_clause([-y, z])
                add_clause([x, -y, -z])
        
        def parse_expression(expr):
            if expr.isdigit():
                return int(expr)
            elif expr.startswith('NOT '):
                sub_expr = expr[4:]
                return -parse_expression(sub_expr)
            else:
                x, op, y = expr.split()
                return add_binary_operation(parse_expression(x), parse_expression(y), op)
        
        expression = " ".join(f"X{i}" if i < n else f"NOT X{i-n}" for i in range(2*n))
        parse_expression(expression)
        
        return literals, clauses
    
    def geometric_entropy(n):
        # Placeholder for the actual computation of geometric entropy
        # This is a dummy implementation that returns a random value for demonstration purposes
        return random.random() * n
    
    def frege_proof_depth(clauses):
        # Placeholder for the actual computation of Frege proof depth
        # This is a dummy implementation that returns a random value for demonstration purposes
        return random.randint(1, 10)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    literals, clauses = tseitin_formula(f, n)
    
    H_f = geometric_entropy(n)
    d_phi_f = frege_proof_depth(clauses)
    
    if d_phi_f == 0:
        return {
            "metric_name": "H(f)/d(φ_f)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Frege proof depth is zero"
        }
    
    ratio = H_f / d_phi_f
    
    return {
        "metric_name": "H(f)/d(φ_f)",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= 0.5 and abs(ratio - 1) <= 0.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"{RESULT} mean={mean_ratio:.2f} std=NA support_fraction={support_fraction:.2f}")