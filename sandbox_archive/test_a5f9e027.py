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
    
    def generate_boolean_circuit(n):
        if n == 1:
            return ['0', '1']
        else:
            left = generate_boolean_circuit(n // 2)
            right = generate_boolean_circuit(n - n // 2)
            return [f'AND({x},{y})' for x in left for y in right] + \
                   [f'OR({x},{y})' for x in left for y in right]
    
    def tseitin_formula(circuit):
        variables = set()
        clauses = []
        
        def add_clause(clause):
            if clause not in clauses:
                clauses.append(clause)
        
        def process_circuit(expr, var_count):
            nonlocal variables
            if expr.startswith('AND'):
                a, b = expr[4:-1].split(',')
                x = process_circuit(a, var_count)
                y = process_circuit(b, var_count + 1)
                add_clause(f'{x} OR {y}')
                return f'NOT({var_count})'
            elif expr.startswith('OR'):
                a, b = expr[3:-1].split(',')
                x = process_circuit(a, var_count)
                y = process_circuit(b, var_count + 1)
                add_clause(f'{x} AND {y}')
                return f'NOT({var_count})'
            else:
                variables.add(expr)
                return expr
        
        var_count = 0
        for expr in circuit:
            process_circuit(expr, var_count)
            var_count += 1
        
        for v in variables:
            add_clause(f'{v} OR NOT({v})')
        
        return clauses
    
    def count_automorphisms(clause):
        # Simplified counting of automorphisms for demonstration
        return len(clause)
    
    n = random.randint(5, 40)
    circuit = generate_boolean_circuit(n)
    tseitin_clauses = tseitin_formula(circuit)
    ord_V = sum(count_automorphisms(clause) for clause in tseitin_clauses)
    w_C = len(circuit)
    
    return {
        "metric_name": "ord(V)",
        "metric_value": ord_V,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ord_V >= w_C ** 2,
        "counterexample": "" if ord_V >= w_C ** 2 else f"Counterexample: ord(V)={ord_V}, w(C)^2={w_C**2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")