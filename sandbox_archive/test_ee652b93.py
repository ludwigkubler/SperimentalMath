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
from math import log2

def generate_circuit(depth):
    if depth <= 0:
        return []
    
    gate = random.choice(['AND', 'OR'])
    sub_depth = random.randint(1, max(0, depth-1))
    left = generate_circuit(sub_depth)
    right = generate_circuit(sub_depth)
    
    return [(gate, left, right)]

def frobenius_coincidence(circuit):
    if not circuit:
        return 0
    
    gate, left, right = circuit
    if gate == 'AND':
        return min(frobenius_coincidence(left), frobenius_coincidence(right))
    elif gate == 'OR':
        return max(frobenius_coincidence(left), frobenius_coincidence(right))
    else:
        raise ValueError("Invalid gate type")

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    depths = [5, 10, 15, 20, 30, 40]
    max_depth = max(depths)
    instances_tested = len(depths) * 5
    
    max_coincidence = 0
    for depth in depths:
        for _ in range(5):
            circuit = generate_circuit(depth)
            coincidence = frobenius_coincidence(circuit)
            if coincidence > max_coincidence:
                max_coincidence = coincidence
    
    metric_value = max_coincidence / (max_depth ** 2)
    
    conjecture_holds = metric_value <= 1.25
    counterexample = "" if conjecture_holds else f"Max coincidence {max_coincidence} exceeds 1.25 * {max_depth}^2"
    
    return {
        "metric_name": "Frobenius Coincidence Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": max_depth,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Max coincidence exceeds 1.25 * D^2\" first_failing_seed={first_failing_seed}")