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
    return [f'({l} AND {r})' for l in left] + [f'({l} OR {r})' for l in right]

def evaluate_circuit(circuit):
    if isinstance(circuit, str):
        return circuit
    else:
        left = evaluate_circuit(circuit[0])
        right = evaluate_circuit(circuit[1])
        op = circuit[2]
        if op == 'AND':
            return '1' if left == '1' and right == '1' else '0'
        elif op == 'OR':
            return '1' if left == '1' or right == '1' else '0'

def construct_noncommutative_algebra(circuit):
    n = 2 ** (len(circuit) - 1)
    generators = [f'a{i}' for i in range(n)]
    relations = []
    
    def add_relation(i, j):
        if i != j:
            relations.append(f'{generators[i]} * {generators[j]} = 0')
    
    def process_circuit(circuit):
        if isinstance(circuit, str):
            return circuit
        else:
            left = process_circuit(circuit[0])
            right = process_circuit(circuit[1])
            op = circuit[2]
            if op == 'AND':
                add_relation(int(left, 2), int(right, 2))
            elif op == 'OR':
                add_relation(int(left, 2) ^ 1, int(right, 2))
            return f'({left} OR {right})'
    
    process_circuit(circuit)
    return generators, relations

def min_rank(generators, relations):
    n = len(generators)
    A = [[0] * n for _ in range(n)]
    
    def multiply(a, b):
        result = [0] * n
        for i in range(n):
            for j in range(n):
                if a[i] and b[j]:
                    result[(i + j) % n] += 1
        return result
    
    def is_zero_vector(v):
        return all(x == 0 for x in v)
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        
        for i in range(n):
            max_row = -1
            for j in range(m):
                if A[j][i] != 0:
                    if max_row == -1 or abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
            
            if max_row == -1:
                continue
            
            A[max_row], A[rank] = A[rank], A[max_row]
            
            for j in range(m):
                if j != rank:
                    factor = A[j][i] / A[rank][i]
                    for k in range(n):
                        A[j][k] -= factor * A[rank][k]
            
            rank += 1
        
        return rank
    
    return gaussian_elimination(A)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    circuit = generate_circuit(n)
    generators, relations = construct_noncommutative_algebra(circuit)
    rank = min_rank(generators, relations)
    
    if rank is None:
        return {
            "metric_name": "min_rank",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    expected_bound = n * math.log(n, 2)
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank <= expected_bound,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results]
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    
    if conjecture_holds:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = len(results) / len(seeds)
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")