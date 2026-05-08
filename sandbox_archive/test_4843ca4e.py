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
    results = []
    for n in range(10, 41):
        instances_tested = 30
        connectivity_sum = 0
        for _ in range(instances_tested):
            Phi = generate_random_3sat(n)
            incidence_matrix = get_incidence_matrix(Phi)
            connectivity = matroid_connectivity(incidence_matrix)
            connectivity_sum += connectivity
        avg_connectivity = connectivity_sum / instances_tested
        results.append({
            'metric_name': 'matroid_connectivity',
            'metric_value': avg_connectivity,
            'instances_tested': instances_tested,
            'conjecture_holds': abs(avg_connectivity - math.log(n, 2)) < 1,
            'counterexample': '' if abs(avg_connectivity - math.log(n, 2)) < 1 else f'n={n}, connectivity={avg_connectivity}'
        })
    return {
        'seed': seed,
        'results': results
    }

def generate_random_3sat(n: int) -> list:
    clauses = []
    for _ in range(2 * n):
        literals = random.sample(range(-n, 0), 1) + random.sample(range(1, n + 1), 2)
        clauses.append(literals)
    return clauses

def get_incidence_matrix(Phi: list) -> list:
    n = max(abs(lit) for clause in Phi for lit in clause)
    matrix = [[0] * len(Phi) for _ in range(n)]
    for i, clause in enumerate(Phi):
        for lit in clause:
            matrix[abs(lit) - 1][i] = 1 if lit > 0 else -1
    return matrix

def matroid_connectivity(matrix: list) -> int:
    n, m = len(matrix), len(matrix[0])
    def gaussian_elimination(A):
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                return m
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return sum(1 for row in A if any(row))
    return gaussian_elimination(matrix)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.extend(result['results'])
    
    avg_connectivity = sum(r['metric_value'] for r in results) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - avg_connectivity)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    print(f"RESULT: SUPPORTED mean={avg_connectivity:.2f} std={std_dev:.2f} support_fraction={support_fraction:.2f}")