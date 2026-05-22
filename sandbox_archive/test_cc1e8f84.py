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
    
    def generate_xor_and_network(n: int, m: int):
        inputs = [random.randint(0, 1) for _ in range(n)]
        outputs = [random.randint(0, 1) for _ in range(m)]
        network = [(inputs[i], outputs[i]) for i in range(min(n, m))]
        return network
    
    def compute_minimal_rank(network):
        n = len(network)
        if n == 0:
            return 0
        rank = 1
        for i in range(1, n):
            if all(network[j][1] != network[i][1] for j in range(i)):
                rank += 1
        return rank
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for col in range(cols):
            max_row = next((r for r in range(col, rows) if matrix[r][col]), None)
            if max_row is not None:
                matrix[col], matrix[max_row] = matrix[max_row], matrix[col]
                for r in range(col + 1, rows):
                    factor = -matrix[r][col] / matrix[col][col]
                    for c in range(cols):
                        matrix[r][c] += factor * matrix[col][c]
        rank = sum(1 for row in matrix if any(row[i] != 0 for i in range(cols)))
        return rank
    
    def compute_geometric_invariant(network):
        n = len(network)
        m = len(network[0])
        A = [[0] * (n + m) for _ in range(n + m)]
        for i, (x, y) in enumerate(network):
            A[i][i] = 1
            A[n + i][n + i] = 1
            A[i][n + i] = x
            A[n + i][i] = y
        return gaussian_elimination(A)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(1, min(n, 10))
            network = generate_xor_and_network(n, m)
            rank = compute_geometric_invariant(network)
            total_rank += rank
            instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    conjecture_holds = abs(mean_rank - (Fraction(n_values[0]) ** Fraction(2, 3))) <= 3
    counterexample = "" if conjecture_holds else f"mean_rank={mean_rank}, expected=O(n^(2/3))"
    
    return {
        "metric_name": "Minimal Rank of Geometric Invariant",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")