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
    
    def parity_circuit_depth(f, n):
        if n == 1:
            return 0
        depth = 1
        for i in range(n):
            if f(i) != f((i + 1) % n):
                depth += 1
        return depth
    
    def quandle_representation(f, n):
        Q = {}
        for i in range(n):
            Q[i] = set()
            for j in range(n):
                if f(j) == f((j + i) % n):
                    Q[i].add(j)
        return Q
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for col in range(n):
            max_row = max(range(col, m), key=lambda r: abs(augmented_matrix[r][col]))
            augmented_matrix[col], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[col]
            if augmented_matrix[col][col] == 0:
                return float('inf')
            for row in range(m):
                if row != col:
                    factor = augmented_matrix[row][col] / augmented_matrix[col][col]
                    for j in range(n + 1):
                        augmented_matrix[row][j] -= factor * augmented_matrix[col][j]
        return sum(1 for row in range(m) if augmented_matrix[row][-1] == 1)
    
    n = random.randint(5, 40)
    f = [random.choice([-1, 1]) for _ in range(n)]
    depth = parity_circuit_depth(f, n)
    Q = quandle_representation(f, n)
    matrix = [[0 if i not in Q[j] else 1 for j in range(n)] for i in range(n)]
    
    min_rank = rank(matrix)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": depth > 0 and 0.5 <= min_rank / depth <= 1.5,
        "counterexample": "" if depth > 0 and 0.5 <= min_rank / depth <= 1.5 else f"depth={depth}, rank={min_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean = sum(result["metric_value"] for result in results) / len(results)
        std = math.sqrt(sum((result["metric_value"] - mean)**2 for result in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = next(result["counterexample"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")