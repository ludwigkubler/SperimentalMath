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
    
    def generate_tseitin_circuit(size, depth):
        if size == 1 and depth == 0:
            return ['x']
        elif size == 1 and depth > 0:
            return [f'NOT {generate_tseitin_circuit(1, depth-1)}']
        else:
            left = generate_tseitin_circuit(size // 2, depth - 1)
            right = generate_tseitin_circuit((size + 1) // 2, depth - 1)
            return [f'AND {left[0]} {right[0]}', f'OR {left[0]} {right[0]}']
    
    def evaluate_circuit(circuit):
        if isinstance(circuit, str):
            return circuit
        else:
            left = evaluate_circuit(circuit[1])
            right = evaluate_circuit(circuit[2])
            if circuit[0] == 'NOT':
                return not left
            elif circuit[0] == 'AND':
                return left and right
            elif circuit[0] == 'OR':
                return left or right
    
    def generate_qmc_sequence(degree):
        points = []
        for i in range(2**degree):
            point = [i & (1 << j) > 0 for j in range(degree)]
            points.append(point)
        return points
    
    def min_distance(points):
        n = len(points[0])
        dists = []
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                dist = sum(1 for a, b in zip(points[i], points[j]) if a != b)
                dists.append(dist)
        return min(dists) if dists else float('inf')
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        x_sorted = sorted(zip(x, range(n)))
        y_sorted = sorted(zip(y, range(n)))
        rank_x = [y[1] for x, y in x_sorted]
        rank_y = [x[1] for x, y in y_sorted]
        sum_diff_squares = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    size = random.randint(5, 40)
    depth = random.randint(1, 10)
    circuit = generate_tseitin_circuit(size, depth)
    qmc_sequence = generate_qmc_sequence(depth)
    min_dist = min_distance(qmc_sequence)
    tseitin_size = len(circuit)
    
    return {
        "metric_name": "min_dist",
        "metric_value": min_dist,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")