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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        pivot = A[i][i]
        if pivot == 0:
            return None
        for j in range(i + 1, m):
            factor = -A[j][i] / pivot
            for k in range(n):
                A[j][k] += factor * A[i][k]
    return A

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for j in range(p):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def sipser_like_function(n, seed):
        random.seed(seed)
        return [random.randint(0, 1) for _ in range(n)]
    
    def sum_product_complexity(A):
        A_plus = set()
        A_dot = set()
        for x in A:
            if x not in A_plus:
                A_plus.add(x)
            if x not in A_dot:
                A_dot.add(tuple(sorted(x)))
        return len(A_plus) * len(A_dot)
    
    def dpll_circuit(f, n):
        def evaluate(circuit, assignment):
            for gate in circuit:
                if gate['type'] == 'AND':
                    result = True
                    for input in gate['inputs']:
                        if not evaluate(input, assignment):
                            result = False
                            break
                    assignment[gate['output']] = result
                elif gate['type'] == 'OR':
                    result = False
                    for input in gate['inputs']:
                        if evaluate(input, assignment):
                            result = True
                            break
                    assignment[gate['output']] = result
                elif gate['type'] == 'NOT':
                    assignment[gate['output']] = not evaluate(gate['input'], assignment)
            return assignment[f]
        
        def backtrack(circuit, assignment):
            if all(assignment[x] is not None for x in f):
                return evaluate(circuit, assignment)
            var = next(x for x in f if assignment[x] is None)
            for val in [True, False]:
                assignment[var] = val
                if backtrack(circuit, assignment):
                    return True
                assignment[var] = None
            return False
        
        circuit = []
        for i in range(2**n):
            inputs = [(i >> j) & 1 for j in range(n)]
            output = f[i]
            if output == 1:
                circuit.append({'type': 'AND', 'inputs': [{'type': 'NOT' if x else 'VAR', 'input': {'output': j}} for j, x in enumerate(inputs)], 'output': i})
        return backtrack(circuit, {x: None for x in f})
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = sipser_like_function(n, seed)
    A = [i for i, x in enumerate(f) if x == 1]
    sp_complexity = sum_product_complexity(A)
    
    if sp_complexity < n**2:
        return {
            "metric_name": "sum_product_complexity",
            "metric_value": sp_complexity,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "function_has_lower_sp_complexity"
        }
    
    acc0_size = 2**(n//2)
    instances_tested = 0
    conjecture_holds = True
    
    for _ in range(30):
        if dpll_circuit(f, n):
            instances_tested += 1
    
    return {
        "metric_name": "sum_product_complexity",
        "metric_value": sp_complexity,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
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
    
    mean_value = sum(r['metric_value'] * r['instances_tested'] for r in results) / sum(r['instances_tested'] for r in results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 * r['instances_tested'] for r in results) / sum(r['instances_tested'] for r in results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"function_has_lower_sp_complexity\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")