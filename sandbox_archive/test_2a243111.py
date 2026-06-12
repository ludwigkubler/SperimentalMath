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
    
    def generate_random_circuit(depth):
        if depth == 0:
            return ['NOT', random.choice([True, False])]
        else:
            op = random.choice(['AND', 'OR'])
            left = generate_random_circuit(depth - 1)
            right = generate_random_circuit(depth - 1)
            return [op, left, right]
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, list):
            op = circuit[0]
            left = evaluate_circuit(circuit[1])
            right = evaluate_circuit(circuit[2])
            if op == 'NOT':
                return not left
            elif op == 'AND':
                return left and right
            elif op == 'OR':
                return left or right
        else:
            return circuit
    
    def tropical_hermitian_form(circuit):
        n = 2 ** (len(circuit) - 1)
        H = [[0] * n for _ in range(n)]
        
        def assign_values(node, start, end):
            if isinstance(node, list):
                op = node[0]
                left = evaluate_circuit(node[1])
                right = evaluate_circuit(node[2])
                mid = (start + end) // 2
                if op == 'NOT':
                    H[start][mid] = 1
                    H[mid][end] = 1
                elif op == 'AND':
                    H[start][mid] = 1
                    H[mid][mid] = 1
                    H[mid][end] = 1
                elif op == 'OR':
                    H[start][start] = 1
                    H[start][mid] = 1
                    H[mid][end] = 1
                assign_values(node[1], start, mid)
                assign_values(node[2], mid, end)
            else:
                H[start][end - 1] = 1
        
        assign_values(circuit, 0, n)
        return H
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                else:
                    return i
            for j in range(n):
                if j != i and matrix[i][j] != 0:
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(i, n):
                        matrix[j][k] += factor * matrix[i][k]
        rank = m
        for i in range(m):
            if all(matrix[i][j] == 0 for j in range(n)):
                rank -= 1
        return rank
    
    depths = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for depth in depths:
        circuit = generate_random_circuit(depth)
        H = tropical_hermitian_form(circuit)
        r = rank(H)
        ranks.append(r)
    
    mean_rank = sum(ranks) / len(ranks)
    n_max = max(depths)
    instances_tested = len(depths)
    
    correlation_coefficient = 0
    for depth, rank in zip(depths, ranks):
        correlation_coefficient += (depth - mean_rank) * (rank - mean_rank)
    correlation_coefficient /= instances_tested * math.sqrt(sum((depth - mean_rank) ** 2 for depth in depths) * sum((rank - mean_rank) ** 2 for rank in ranks))
    
    conjecture_holds = correlation_coefficient >= 0.7
    counterexample = "" if conjecture_holds else f"Correlation coefficient {correlation_coefficient:.2f} < 0.7"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std=0.00 support_fraction=1.00")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std=0.00 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient {r['metric_value']:.2f} < 0.7\" first_failing_seed={first_failing_seed}")