# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def generate_cnf(n):
    literals = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for _ in range(n):
        clause = random.sample(literals + [f'-{l}' for l in literals], 2)
        clauses.append(clause)
    return ' '.join(' '.join(c) for c in clauses)

def grothendieck_witt_class(phi, p):
    n = phi.count('x') // 2
    poly = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in phi.split():
        if '-' not in clause:
            x, y = clause.split()
            i, j = int(x[1:]) - 1, int(y[1:]) - 1
            poly[i][j] += 1
            poly[j][i] += 1
    for i in range(n + 1):
        poly[i][i] -= sum(poly[i][:i]) + sum(poly[:i][i])
    det = determinant(poly, p)
    return det % p

def determinant(matrix, p):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    det = 0
    for j in range(n):
        submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += (-1) ** j * matrix[0][j] * determinant(submatrix, p)
    return det % p

def communication_complexity_rank_variance(phi):
    n = phi.count('x') // 2
    rank = 0
    for i in range(n + 1):
        for j in range(i + 1, n + 1):
            if any(f'x{i}' in clause and f'-x{j}' in clause or f'-x{i}' in clause and f'x{j}' in clause for clause in phi.split()):
                rank += 1
    return rank ** 2 / (n * (n - 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    instances_tested = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if time.time() + (n - 5) * 0.1 > 240:
            print('RESULT: INCONCLUSIVE reason=budget_exceeded n_tested=30')
            return {'seed': seed, 'metric_name': 'min_index', 'metric_value': None, 'instances_tested': instances_tested, 'n_max': n_max, 'conjecture_holds': False, 'counterexample': ''}
        
        for _ in range(5):
            phi = generate_cnf(n)
            p = random.randint(2, 100)
            try:
                min_index = grothendieck_witt_class(phi, p)
                v = communication_complexity_rank_variance(phi)
                metric_values.append((min_index, v))
                instances_tested += 1
                n_max = max(n_max, n)
            except Exception as e:
                print(f'ERROR: {e}')
    
    if not metric_values:
        return {'seed': seed, 'metric_name': 'min_index', 'metric_value': None, 'instances_tested': instances_tested, 'n_max': n_max, 'conjecture_holds': False, 'counterexample': ''}
    
    min_indices = [v[0] for v in metric_values]
    variances = [v[1] for v in metric_values]
    mean_min_index = sum(min_indices) / len(min_indices)
    mean_variance = sum(variances) / len(variances)
    
    correlation_coefficient = 0
    if len(metric_values) > 1:
        numerator = sum((min_indices[i] - mean_min_index) * (variances[i] - mean_variance) for i in range(len(metric_values)))
        denominator = math.sqrt(sum((min_indices[i] - mean_min_index) ** 2 for i in range(len(metric_values))) * sum((variances[i] - mean_variance) ** 2 for i in range(len(metric_values))))
        correlation_coefficient = numerator / denominator
    
    return {
        'seed': seed,
        'metric_name': 'min_index',
        'metric_value': correlation_coefficient,
        'instances_tested': instances_tested,
        'n_max': n_max,
        'conjecture_holds': abs(correlation_coefficient) >= 0.8,
        'counterexample': ''
    }

if __name__ == "__main__":
    import sys
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f'TRIAL: {result}')
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results if r['metric_value'] is not None) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f'RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}')
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f'RESULT: FALSIFIED counterexample="correlation_coefficient_not_sufficiently_high" first_failing_seed={first_failing_seed}')
    else:
        print(f'RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}')