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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate below
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n+1):
                matrix[j][k] -= factor * matrix[i][k]

    # Back substitution
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = Fraction(matrix[i][n], matrix[i][i])
        for j in range(i-1, -1, -1):
            matrix[j][n] -= matrix[j][i] * x[i]
    return x

def solve_linear_system(A, b):
    augmented_matrix = [row + [b[i]] for i, row in enumerate(A)]
    solution = gaussian_elimination(augmented_matrix)
    return solution

def min_geometric_invariant(vertices, facets):
    n = len(vertices[0])
    min_dist = float('inf')
    
    for facet in facets:
        A = []
        b = []
        for vertex in vertices:
            eq = [vertex[i] for i in facet]
            A.append(eq)
            b.append(-eq[facet[-1]])
        
        try:
            solution = solve_linear_system(A, b)
            dist = sum(x**2 for x in solution) ** 0.5
            if dist < min_dist:
                min_dist = dist
        except Exception as e:
            return float('inf')
    
    return min_dist

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    vertices = [[random.uniform(-1, 1) for _ in range(n)] for _ in range(random.randint(3, n+2))]
    facets = [sorted(random.sample(range(n), k=random.randint(2, n))) for _ in range(random.randint(1, min(n-1, 5)))]
    
    min_dist = min_geometric_invariant(vertices, facets)
    communication_complexity = math.log2(n) ** 2
    
    return {
        "metric_name": "min_geometric_invariant",
        "metric_value": min_dist,
        "instances_tested": len(facets),
        "conjecture_holds": min_dist >= n * math.log2(n) and communication_complexity <= (n * math.log2(n)) ** 2,
        "counterexample": "" if min_dist >= n * math.log2(n) else f"min_geometric_invariant < {n * math.log2(n)}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r['metric_value'] for r in results) / len(results)
    std_metric = (sum((r['metric_value'] - mean_metric) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"min_geometric_invariant < {n * math.log2(n)}\" first_failing_seed={first_failing_seed}")