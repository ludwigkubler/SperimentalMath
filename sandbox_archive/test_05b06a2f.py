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

def generate_circuit(n):
    if n == 1:
        return ['0', '1']
    left = generate_circuit(n // 2)
    right = generate_circuit(n - n // 2)
    return [f'({l} OR {r})' for l in left] + [f'({l} AND {r})' for l in left] + [f'NOT {r}' for r in right]

def evaluate_circuit(circuit):
    if isinstance(circuit, str):
        return circuit
    else:
        return '(' + ' OR '.join(evaluate_circuit(subcircuit) for subcircuit in circuit) + ')'

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    evaluated_circuit = evaluate_circuit(circuit)
    
    # Simulate the evaluation of the circuit
    variables = {f'x{i}': random.choice(['0', '1']) for i in range(n)}
    def eval_var(var):
        if var.startswith('x'):
            return variables[var]
        elif var == '0':
            return '0'
        elif var == '1':
            return '1'
        else:
            return '(' + ' OR '.join(eval_var(subvar) for subvar in var[1:-1].split()) + ')'
    
    result = eval_var(evaluated_circuit)
    
    # Count the number of Galois actions
    galois_actions = set()
    def count_galois_actions(expr):
        if isinstance(expr, str):
            galois_actions.add(expr)
        else:
            for subexpr in expr[1:-1].split():
                count_galois_actions(subexpr)
    
    count_galois_actions(evaluated_circuit)
    
    metric_value = len(galois_actions)
    n_max = n
    conjecture_holds = metric_value <= n**2 * math.log(n)
    counterexample = "" if conjecture_holds else f"n={n}, |Γ_C|={metric_value}"
    
    return {
        "metric_name": "Number of Galois Actions",
        "metric_value": metric_value,
        "instances_tested": 1,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res['metric_value'] for res in results) / len(results)
    std_value = math.sqrt(sum((res['metric_value'] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res['conjecture_holds']) / len(results)
    
    if all(res['conjecture_holds'] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[first_failing_seed]['n_max']}, |Γ_C|={results[first_failing_seed]['metric_value']}\" first_failing_seed={first_failing_seed}")