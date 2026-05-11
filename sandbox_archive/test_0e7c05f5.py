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

def gaussian_elimination(A, b):
    n = len(b)
    for i in range(n):
        max_row = i + max(range(i, n), key=lambda j: abs(A[j][i]))
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            A[j] = [A[j][k] - factor * A[i][k] for k in range(n)]
            b[j] -= factor * b[i]
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x

def poly_to_matrix(poly, variables):
    n = len(variables)
    m = len(poly)
    A = [[0] * n for _ in range(m)]
    b = [0] * m
    for i, p in enumerate(poly):
        terms = p.split('*')
        for term in terms:
            if '!' not in term:
                continue
            var = term[1:-2]
            A[i][variables.index(var)] += 1
        b[i] = -1
    return A, b

def sos_degree(poly, variables):
    n = len(variables)
    m = len(poly)
    A, b = poly_to_matrix(poly, variables)
    try:
        x = gaussian_elimination(A, b)
        return max(abs(x_i) for x_i in x)
    except Exception as e:
        return float('inf')

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = 3 * n
    variables = [f'x{i}' for i in range(n)]
    clauses = ['!(x{}*x{}*{})'.format(*random.sample(variables, 3)) for _ in range(m)]
    poly = [c.replace('!', '') for c in clauses]
    degree = sos_degree(poly, variables)
    expected_degree = math.isclose(degree, math.sqrt(m), rel_tol=1e-2)
    return {
        "metric_name": "SOS Degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": expected_degree,
        "counterexample": "" if expected_degree else f"Expected degree {math.sqrt(m)}, got {degree}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_degree = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_degree)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_degree} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_degree} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")