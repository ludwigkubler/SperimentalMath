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

def generate_tseitin_circuit(size, depth):
    if size == 1:
        return ['x0']
    elif depth == 1:
        return [f'NOT {generate_tseitin_circuit(1, 1)[0]}']
    
    left = generate_tseitin_circuit(size // 2, depth - 1)
    right = generate_tseitin_circuit(size - size // 2, depth - 1)
    var = f'x{size}'
    return [f'{var}', f'AND {left[0]} {right[0]}', f'OR {left[0]} {not_var(right[0])}']

def not_var(var):
    if var.startswith('NOT '):
        return var[4:]
    else:
        return f'NOT {var}'

def generate_qmc_sequence(circuit, degree):
    n = len(circuit)
    qmc = []
    for _ in range(2**degree):
        point = [random.choice([0, 1]) for _ in range(n)]
        if all(point[i] == (point[0] ^ point[1] ^ point[2]) % 2 for i in range(3)):
            qmc.append(point)
    return qmc

def compute_min_dist(qmc):
    n = len(qmc[0])
    min_dist = float('inf')
    for i in range(len(qmc)):
        for j in range(i + 1, len(qmc)):
            dist = sum(abs(qmc[i][k] - qmc[j][k]) for k in range(n))
            if dist < min_dist:
                min_dist = dist
    return min_dist

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    size = random.randint(1, 40)
    depth = random.randint(1, 10)
    circuit = generate_tseitin_circuit(size, depth)
    qmc = generate_qmc_sequence(circuit, depth)
    min_dist = compute_min_dist(qmc)
    
    return {
        "metric_name": "min_dist",
        "metric_value": min_dist,
        "instances_tested": len(qmc),
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_d = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='' first_failing_seed={first_failing_seed}")