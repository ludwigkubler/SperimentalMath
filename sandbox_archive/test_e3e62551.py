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
    
    def generate_circuit(depth, n):
        if depth == 1:
            return [random.choice(['0', '1'])]
        else:
            subcircuits = [generate_circuit(random.randint(1, depth-1), n) for _ in range(2)]
            gate = random.choice(['AND', 'OR'])
            return [gate] + subcircuits
    
    def evaluate_circuit(circuit):
        if isinstance(circuit[0], str):
            return circuit
        else:
            left = evaluate_circuit(circuit[1])
            right = evaluate_circuit(circuit[2])
            gate = circuit[0]
            if gate == 'AND':
                return [left, right] if all(eval(x) for x in (left, right)) else ['0']
            elif gate == 'OR':
                return [left, right] if any(eval(x) for x in (left, right)) else ['1']
    
    def tautological_ideal(circuit):
        n = len(circuit)
        variables = list('x' + str(i) for i in range(n))
        equations = []
        for expr in evaluate_circuit(circuit):
            if expr == '0':
                equation = [1] * n
                for i, var in enumerate(variables):
                    if var not in expr:
                        equation[i] = -1
                equations.append(equation)
            elif expr == '1':
                continue
        return equations
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def minimal_geometric_entropy(ideal):
        m, n = len(ideal), len(ideal[0])
        rank = 0
        for row in ideal:
            if any(row):
                rank += 1
        return rank * math.log(n)
    
    def pearson_correlation(X, Y):
        mean_X = sum(X) / len(X)
        mean_Y = sum(Y) / len(Y)
        cov = sum((x - mean_X) * (y - mean_Y) for x, y in zip(X, Y)) / len(X)
        std_X = math.sqrt(sum((x - mean_X)**2 for x in X) / len(X))
        std_Y = math.sqrt(sum((y - mean_Y)**2 for y in Y) / len(Y))
        return cov / (std_X * std_Y)
    
    def generate_seeds(n):
        seeds = [random.randint(0, 10**9) for _ in range(n)]
        return seeds
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_instances = 0
    max_n = 0
    
    for n in n_values:
        instances_tested = 0
        H_min_values = []
        d_values = []
        
        for _ in range(10):
            depth = random.randint(2, n)
            circuit = generate_circuit(depth, n)
            ideal = tautological_ideal(circuit)
            H_min = minimal_geometric_entropy(ideal)
            instances_tested += 1
            max_n = max(max_n, n)
            
            if H_min is not None:
                H_min_values.append(H_min)
                d_values.append(depth**2 * math.log(n))
        
        results.append({
            "metric_name": "minimal_geometric_entropy",
            "metric_value": sum(H_min_values) / len(H_min_values),
            "instances_tested": instances_tested,
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": ""
        })
    
    mean_H_min = sum(result["metric_value"] for result in results) / len(results)
    std_H_min = math.sqrt(sum((result["metric_value"] - mean_H_min)**2 for result in results) / len(results))
    correlation_coefficient = pearson_correlation([r["metric_value"] for r in results], [r["instances_tested"] for r in results])
    
    if correlation_coefficient >= 0.9:
        support_fraction = sum(1 for r in results if abs(r["metric_value"] - (r["instances_tested"]**2 * math.log(r["n_max"]))) <= 0.1 * (r["instances_tested"]**2 * math.log(r["n_max"]))) / len(results)
        if support_fraction >= 0.95:
            print(f"RESULT: SUPPORTED mean={mean_H_min} std={std_H_min} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='correlation_coefficient' first_failing_seed=1")
    else:
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient' first_failing_seed=1")

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 10**9) for _ in range(30)]
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")