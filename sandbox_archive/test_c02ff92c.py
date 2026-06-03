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

def generate_random_boolean_circuit(n: int) -> list:
    circuit = []
    for _ in range(2 ** n):
        gate = random.choice(['AND', 'OR', 'NOT'])
        inputs = [random.randint(0, 1) for _ in range(n)]
        circuit.append((gate, inputs))
    return circuit

def truth_table(circuit: list) -> dict:
    table = {}
    n = len(next(iter(circuit))[1])
    for i in range(2 ** n):
        inputs = [i >> j & 1 for j in range(n)]
        output = evaluate_circuit(circuit, inputs)
        table[tuple(inputs)] = output
    return table

def evaluate_circuit(circuit: list, inputs: list) -> int:
    stack = []
    for gate, inputs in circuit:
        if gate == 'NOT':
            stack.append(1 - inputs[0])
        elif gate == 'AND':
            result = 1
            for i in inputs:
                result &= i
            stack.append(result)
        elif gate == 'OR':
            result = 0
            for i in inputs:
                result |= i
            stack.append(result)
    return stack[-1]

def polynomial_from_truth_table(table: dict) -> str:
    variables = list(table.keys())[0]
    n = len(variables)
    terms = []
    for inputs, output in table.items():
        if output == 1:
            term = ' + '.join(f'x{i+1}' if inputs[i] else f'(1 - x{i+1})' for i in range(n))
            terms.append(term)
    polynomial = ' * '.join(terms)
    return polynomial

def diophantine_degree(polynomial: str) -> int:
    degree = 0
    for term in polynomial.split(' + '):
        if '*' in term:
            factors = term.split(' * ')
            degree = max(degree, sum(factors.count(f'x{i+1}') for i in range(len(factors))))
    return degree

def min_diophantine_degree(circuit: list) -> int:
    table = truth_table(circuit)
    polynomial = polynomial_from_truth_table(table)
    return diophantine_degree(polynomial)

def monotone_width(circuit: list) -> int:
    n = len(next(iter(circuit))[1])
    max_width = 0
    for i in range(2 ** n):
        inputs = [i >> j & 1 for j in range(n)]
        width = sum(inputs)
        if width > max_width:
            max_width = width
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        circuit = generate_random_boolean_circuit(n)
        degree = min_diophantine_degree(circuit)
        width = monotone_width(circuit)
        results.append((degree, width))
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No circuits generated"
        }
    
    degrees = [r[0] for r in results]
    widths = [r[1] for r in results]
    mean_degree = sum(degrees) / len(degrees)
    mean_width = sum(widths) / len(widths)
    correlation = (sum((d - mean_degree) * (w - mean_width) for d, w in results) /
                   math.sqrt(sum((d - mean_degree) ** 2 for d in degrees) *
                             sum((w - mean_width) ** 2 for w in widths)))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _ in results),
        "conjecture_holds": correlation >= 0.7,
        "counterexample": "" if correlation >= 0.7 else f"Correlation too low: {correlation:.2f}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"Correlation too low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")