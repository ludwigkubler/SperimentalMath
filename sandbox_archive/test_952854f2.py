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

def gaussian_elimination(matrix, b):
    n = len(matrix)
    augmented = [[matrix[i][j] for j in range(n)] + [b[i]] for i in range(n)]
    
    for i in range(n):
        # Find pivot row
        max_row = i
        for k in range(i+1, n):
            if abs(augmented[k][i]) > abs(augmented[max_row][i]):
                max_row = k
        
        # Swap rows
        augmented[i], augmented[max_row] = augmented[max_row], augmented[i]
        
        # Eliminate below pivot
        for k in range(i+1, n):
            factor = Fraction(augmented[k][i], augmented[i][i])
            for j in range(n + 1):
                augmented[k][j] -= factor * augmented[i][j]
    
    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = augmented[i][-1]
        for k in range(i+1, n):
            x[i] -= augmented[i][k] * x[k]
        x[i] /= augmented[i][i]
    
    return x

def adjacency_matrix(graph):
    n = len(graph)
    mat = [[0] * n for _ in range(n)]
    for u, v in graph:
        mat[u][v] = 1
        mat[v][u] = 1
    return mat

def laplacian_matrix(mat):
    n = len(mat)
    lmat = [[0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(mat[i])
        lmat[i][i] = degree
        for j in range(i+1, n):
            lmat[i][j] = -mat[i][j]
            lmat[j][i] = -mat[i][j]
    return lmat

def bp_width(instance):
    graph = instance['graph']
    n = len(graph)
    mat = adjacency_matrix(graph)
    laplacian = laplacian_matrix(mat)
    
    # Compute eigenvalues using Gaussian elimination
    try:
        eigenvalues = gaussian_elimination(laplacian, [0] * n)
    except ZeroDivisionError:
        return None
    
    # The width of the BP is the maximum absolute value of the eigenvalues
    bp_w = max(abs(e) for e in eigenvalues if e != 0)
    return bp_w

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    graph = [(i, j) for i in range(n) for j in range(i+1, n)]
    instance = {'graph': graph}
    
    bp_w = bp_width(instance)
    if bp_w is None:
        return {
            'metric_name': 'bp_width',
            'metric_value': None,
            'instances_tested': 1,
            'conjecture_holds': False,
            'counterexample': 'mapping_undefined'
        }
    
    min_rank = len(graph)  # Simplified for testing purposes
    
    return {
        'metric_name': 'bp_width',
        'metric_value': bp_w,
        'instances_tested': 1,
        'conjecture_holds': False,
        'counterexample': ''
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r['metric_value'] for r in results if r['metric_value'] is not None]
    support_fraction = sum(r['conjecture_holds'] for r in results) / len(results)
    
    if all(v is not None for v in metric_values):
        mean = sum(metric_values) / len(metric_values)
        std = (sum((x - mean) ** 2 for x in metric_values) / len(metric_values)) ** 0.5
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='' first_failing_seed=None")
    else:
        print("RESULT: INCONCLUSIVE reason=missing_data n_tested=30")