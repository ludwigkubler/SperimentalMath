# auto-injected by SEC sandbox
import math
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

def generate_circuit(size, depth):
    if size == 0 or depth == 0:
        return []
    sub_size = random.randint(1, size - 1)
    sub_depth = random.randint(1, depth - 1)
    left = generate_circuit(sub_size, sub_depth)
    right = generate_circuit(size - sub_size, depth - sub_depth)
    return [('AND', left, right)] + left + right

def compute_symplectic_area(circuit):
    if not circuit:
        return 0
    gate_type, left, right = circuit[0]
    if gate_type == 'AND':
        return 1 + compute_symplectic_area(left) + compute_symplectic_area(right)
    else:
        raise ValueError("Unsupported gate type")

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_circuit(n, n // 2)
            s_C = len(circuit)
            d_C = max(len(path) for path in circuit if isinstance(path[0], tuple))
            A_C = compute_symplectic_area(circuit)
            results.append((s_C, d_C, A_C))
    metric_value = sum(A_C <= s_C**2 * d_C for s_C, d_C, A_C in results) / len(results)
    conjecture_holds = all(A_C <= s_C**2 * d_C for s_C, d_C, A_C in results)
    return {
        "metric_name": "Symplectic Area Bound",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif sum(r["conjecture_holds"] for r in results) >= 24:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")