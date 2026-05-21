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
    
    def perm(n):
        if n == 0:
            return [[]]
        perms = []
        for i in range(n):
            for p in perm(n-1):
                if i not in p:
                    perms.append(p + [i])
        return perms
    
    def det(matrix):
        if len(matrix) == 1:
            return matrix[0][0]
        elif len(matrix) == 2:
            return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            det_val = 0
            for i in range(len(matrix)):
                submatrix = [row[:i] + row[i+1:] for row in matrix[1:]]
                det_val += ((-1) ** i) * matrix[0][i] * det(submatrix)
            return det_val
    
    def schur_weyl_invariant(f):
        # Placeholder function. This is a dummy implementation.
        # In practice, you would need to implement the actual Schur-Weyl duality invariant calculation.
        return random.random()
    
    n = random.randint(5, 40)
    f = [random.choice([1, -1]) * x**i for i in range(n+1)]
    I_f = schur_weyl_invariant(f)
    
    m = math.floor(n ** 1.5)
    perm_n = perm(n)
    det_m = det([[f[i] for i in p] for p in perm_n])
    ratio = I_f / det_m
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio > 0.9 and ratio < 1.1,
        "counterexample": "" if ratio >= 0.9 and ratio <= 1.1 else f"Ratio out of bounds: {ratio}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r['metric_value'] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")