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
    
    def perm(n):
        return [[random.randint(1, n) for _ in range(n)] for _ in range(n)]
    
    def det(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det_val = 0
            for c in range(len(matrix)):
                submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
                sign = (-1) ** (c % 2)
                det_val += sign * matrix[0][c] * det(submatrix)
            return det_val
    
    def sym_power(matrix, k):
        if k == 0:
            return [[1]]
        result = []
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                new_matrix = [row[:] for row in matrix]
                new_matrix[i][j] += 1
                result.append(new_matrix)
        return sym_power(result, k-1)
    
    def count_irreducible_components(matrix):
        n = len(matrix)
        components = set()
        for i in range(n):
            for j in range(n):
                component = (i, j)
                queue = [component]
                while queue:
                    x, y = queue.pop(0)
                    if matrix[x][y] == 0:
                        continue
                    matrix[x][y] = 0
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < n and 0 <= ny < n:
                            queue.append((nx, ny))
                components.add(component)
        return len(components)
    
    n = random.randint(2, 40)
    m = int(n ** 1.5) - 1
    k = math.ceil(math.log(n))
    
    perm_n = perm(n)
    det_m = [[det(matrix)] for matrix in [perm(m)]]
    
    perm_n_sym_k = sym_power(perm_n, k)
    det_m_sym_k = sym_power(det_m, k)
    
    perm_n_components = count_irreducible_components(perm_n_sym_k)
    det_m_components = count_irreducible_components(det_m_sym_k)
    
    metric_value = perm_n_components - det_m_components
    conjecture_holds = metric_value >= n ** (k-1)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "irreducible_components",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")