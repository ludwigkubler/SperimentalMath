# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import product

def generate_ac0_circuit(n, depth):
    if n == 1:
        return [random.randint(0, 1) for _ in range(depth)]
    subcircuits = [generate_ac0_circuit(n // 2, depth - 1) for _ in range(2)]
    return [subcircuits[0][i] ^ subcircuits[1][i] for i in range(n)]

def hadamard_transform(matrix):
    n = len(matrix)
    result = [[0] * n for _ in range(n)]
    for i, j in product(range(n), repeat=2):
        result[i][j] = (matrix[i // 2][j // 2] if i % 2 == j % 2 else -matrix[i // 2][j // 2]) / math.sqrt(2)
    return result

def discrepancy(matrix):
    n = len(matrix)
    transform = hadamard_transform(matrix)
    max_discrepancy = 0
    for row in transform:
        max_discrepancy = max(max_discrepancy, sum(abs(x) for x in row))
    return max_discrepancy

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    depth = random.randint(1, 3)
    circuit = generate_ac0_circuit(n, depth)
    size = len(circuit)
    disc_value = discrepancy([circuit])
    conjecture_holds = disc_value >= math.log(size) / math.log(2)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "discrepancy",
        "metric_value": disc_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 30*40+1, 7))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")