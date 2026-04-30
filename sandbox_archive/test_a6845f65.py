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

def matrix_mult(A, B):
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    return C

def det(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    elif n == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    else:
        det_val = 0
        for c in range(n):
            sub_matrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            sign = (-1) ** (c % 2)
            sub_det = det(sub_matrix)
            det_val += sign * matrix[0][c] * sub_det
        return det_val

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    s = 2 ** n
    epsilon = 1e-3
    
    # Construct a read-twice branching program
    M_P = [[0] * (2 ** n) for _ in range(2 ** n)]
    for i in range(n):
        for j in range(2 ** (i + 1)):
            M_P[j][j ^ (1 << i)] = random.random()
    
    # Compute the free entropy
    det_val = det(M_P + [[epsilon if i == j else 0 for j in range(2 ** n)] for i in range(2 ** n)])
    phi_M_P = (1 / n) * math.log(det_val)
    
    # Check the conjecture
    conjecture_holds = phi_M_P <= math.log(s)
    counterexample = "" if conjecture_holds else "read-twice BP"
    
    return {
        "metric_name": "free_entropy",
        "metric_value": phi_M_P,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_phi = sum(r['metric_value'] for r in results) / len(results)
    std_phi = math.sqrt(sum((r['metric_value'] - mean_phi) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_phi:.6f} std={std_phi:.6f} support_fraction={support_fraction:.2f}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")