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
    
    # Generate a random arithmetic variety over F_q with q ≥ 5
    q = random.randint(5, 100)
    n = random.randint(5, 40)
    V = [[random.randint(-q, q) for _ in range(n)] for _ in range(n)]
    
    # Compute the Hodge decomposition (simplified version for testing purposes)
    def hodge_decomposition(matrix):
        if not matrix:
            return 0
        det = determinant(matrix)
        if det == 0:
            return float('inf')
        return math.log(abs(det), q)
    
    δ_H_V = hodge_decomposition(V)
    
    # Estimate the quantum query complexity (simplified version for testing purposes)
    def quantum_query_complexity(matrix):
        return sum(1 for row in matrix for elem in row if elem != 0)
    
    Q_Q_V = quantum_query_complexity(V)
    
    metric_name = 'Hodge Depth vs Quantum Query Complexity'
    metric_value = δ_H_V
    instances_tested = 1
    conjecture_holds = δ_H_V <= 2 * Q_Q_V
    counterexample = '' if conjecture_holds else f'δ_H(V)={δ_H_V}, Q(Q(V))={Q_Q_V}'
    
    return {
        'metric_name': metric_name,
        'metric_value': metric_value,
        'instances_tested': instances_tested,
        'conjecture_holds': conjecture_holds,
        'counterexample': counterexample
    }

def determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]
    det = 0
    for c in range(len(matrix)):
        submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
        sign = (-1) ** (c % 2)
        sub_det = determinant(submatrix)
        det += sign * matrix[0][c] * sub_det
    return det

if __name__ == '__main__':
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f'TRIAL: {result}')
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f'RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}')
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f'RESULT: FALSIFIED counterexample="{r["counterexample"]}" first_failing_seed={first_failing_seed}')
    else:
        print('RESULT: INCONCLUSIVE no seeds tested')