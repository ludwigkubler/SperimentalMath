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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR', 'NOT'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            if gate == 'NOT':
                inputs = inputs[:1]
            circuit.append((gate, inputs))
        return circuit
    
    def truth_table(circuit):
        n = len(circuit[0][1])
        table = {}
        for i in range(2**n):
            inputs = [i >> j & 1 for j in range(n)]
            output = evaluate_circuit(circuit, inputs)
            table[tuple(inputs)] = output
        return table
    
    def evaluate_circuit(circuit, inputs):
        stack = []
        for gate, inputs in circuit:
            if gate == 'NOT':
                stack.append(1 - inputs[0])
            elif gate == 'AND':
                stack.append(all(stack[-len(inputs):]))
            elif gate == 'OR':
                stack.append(any(stack[-len(inputs):]))
        return stack.pop()
    
    def min_polynomial(truth_table):
        n = len(next(iter(truth_table)))
        variables = [f'x{i}' for i in range(n)]
        terms = []
        for inputs, output in truth_table.items():
            term = '1' if output else '0'
            for var, val in zip(variables, inputs):
                if val == 0:
                    term += f'*{var}'
                elif val == 1:
                    term += f'*{var}^2'
            terms.append(term)
        polynomial = '+'.join(terms)
        return polynomial
    
    def diophantine_degree(polynomial):
        degree = 0
        for term in polynomial.split('+'):
            if '^' in term:
                _, exp = term.split('^')
                degree = max(degree, int(exp))
        return degree
    
    def monotone_width(circuit):
        n = len(circuit[0][1])
        width = [0] * (n + 1)
        for gate, inputs in circuit:
            if gate == 'NOT':
                width[len(inputs)] += 1
            elif gate == 'AND' or gate == 'OR':
                width[len(inputs) - 1] += 1
        return max(width)
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return None
            pivot = matrix[i][i]
            for j in range(n):
                matrix[i][j] /= pivot
            for j in range(m):
                if j == i:
                    continue
                factor = matrix[j][i]
                for k in range(n):
                    matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rref = gaussian_elimination(matrix)
        if rref is None:
            return 0
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank
    
    def min_diophantine_degree(circuit):
        truth_table_ = truth_table(circuit)
        polynomial = min_polynomial(truth_table_)
        degree = diophantine_degree(polynomial)
        return degree
    
    n_values = [5, 10, 15, 20, 30, 40]
    degrees = []
    widths = []
    
    for n in n_values:
        circuit = generate_random_circuit(n)
        degree = min_diophantine_degree(circuit)
        width = monotone_width(circuit)
        degrees.append(degree)
        widths.append(width)
    
    if not degrees or not widths:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    n = len(degrees)
    sum_degrees = sum(degrees)
    sum_widths = sum(widths)
    sum_degrees_squared = sum(d**2 for d in degrees)
    sum_widths_squared = sum(w**2 for w in widths)
    sum_products = sum(d * w for d, w in zip(degrees, widths))
    
    mean_degree = sum_degrees / n
    mean_width = sum_widths / n
    covariance = (sum_products - n * mean_degree * mean_width) / (n - 1)
    variance_degrees = (sum_degrees_squared - n * mean_degree**2) / (n - 1)
    variance_widths = (sum_widths_squared - n * mean_width**2) / (n - 1)
    
    if variance_degrees == 0 or variance_widths == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = covariance / (math.sqrt(variance_degrees) * math.sqrt(variance_widths))
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.7 and correlation < 0.8,
        "counterexample": "" if correlation >= 0.7 else f"correlation={correlation}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" in r and not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")