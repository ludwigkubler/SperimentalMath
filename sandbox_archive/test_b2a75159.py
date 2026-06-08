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
    
    def generate_boolean_circuit(depth):
        if depth == 1:
            return ['0', '1']
        else:
            left = generate_boolean_circuit(depth - 1)
            right = generate_boolean_circuit(depth - 1)
            return [f'({l} AND {r})' for l in left] + [f'({l} OR {r})' for l in left]
    
    def tseitin_formula(circuit):
        variables = set()
        clauses = []
        
        def encode(var, expr):
            if var not in variables:
                variables.add(var)
                clauses.append([var])
            if expr.startswith('(') and expr.endswith(')'):
                op, a, b = expr[1:-1].split()
                if op == 'AND':
                    encode(f'~{a}', f'{b} OR ~{a}')
                    encode(f'~{b}', f'{a} OR ~{b}')
                    clauses.append([f'~{a}', f'~{b}', var])
                elif op == 'OR':
                    encode(f'~{a}', f'{b} AND ~{a}')
                    encode(f'~{b}', f'{a} AND ~{b}')
                    clauses.append([f'~{a}', f'~{b}', f'~{var}'])
        
        for expr in circuit:
            var = random.choice('abcdefghijklmnopqrstuvwxyz')
            encode(var, expr)
        
        return variables, clauses
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        rank = 0
        
        for i in range(cols):
            pivot_row = next((r for r in range(rank, rows) if matrix[r][i] != 0), None)
            if pivot_row is not None:
                matrix[pivot_row], matrix[rank] = matrix[rank], matrix[pivot_row]
                for j in range(i + 1, cols):
                    factor = -matrix[rank][j] / matrix[rank][i]
                    for k in range(rows):
                        matrix[k][j] += factor * matrix[k][i]
                rank += 1
        
        return rank
    
    def minimal_local_index(clauses):
        n = len(clauses)
        m = len(variables)
        
        # Create augmented matrix
        A = [[0] * (m + n) for _ in range(m)]
        b = [0] * m
        
        for i, clause in enumerate(clauses):
            for var in variables:
                if var in clause:
                    A[i][variables.index(var)] += 1
                elif f'~{var}' in clause:
                    A[i][variables.index(var)] -= 1
        
        rank = gaussian_elimination(A)
        
        return m - rank
    
    depths = [5, 10, 15, 20, 30, 40]
    results = []
    
    for depth in depths:
        circuit = generate_boolean_circuit(depth)
        variables, clauses = tseitin_formula(circuit)
        
        if not clauses or len(variables) == 0:
            return {
                "metric_name": "minimal_local_index",
                "metric_value": None,
                "instances_tested": 1,
                "n_max": depth,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        msl = minimal_local_index(clauses)
        results.append(msl)
    
    mean_msl = sum(results) / len(results)
    max_msl = max(results)
    
    if any(msl > 4 * depth * math.log(len(variables)) for depth, msl in zip(depths, results)):
        return {
            "metric_name": "minimal_local_index",
            "metric_value": mean_msl,
            "instances_tested": len(depths),
            "n_max": max(depths[-1], 40),
            "conjecture_holds": False,
            "counterexample": "local_index_exceeds_bound"
        }
    
    return {
        "metric_name": "minimal_local_index",
        "metric_value": mean_msl,
        "instances_tested": len(depths),
        "n_max": max(depths[-1], 40),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_msl = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_msl = math.sqrt(sum((r['metric_value'] - mean_msl) ** 2 for r in results if r['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_msl} std={std_msl} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and any(r['metric_value'] < 0.5 * depth * math.log(len(variables)) for depth, variables, msl in zip(depths, [set(circuit.split()) for circuit in generate_boolean_circuit(40)], results)):
        print(f"RESULT: FALSIFIED counterexample=\"local_index_exceeds_bound\" first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")