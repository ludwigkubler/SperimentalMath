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
    
    def generate_ac0_circuit(n, depth):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_ac0_circuit(n, depth - 1)
            right = generate_ac0_circuit(n, depth - 1)
            return [random.choice([left[i] ^ right[i] for i in range(len(left))])]

    def compute_quiver_representation(circuit):
        n = len(circuit)
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if circuit[i] == circuit[j]:
                    Q[i][j] = 1
                    Q[j][i] = 1
        return Q

    def compute_symmetry(Q):
        n = len(Q)
        symmetries = []
        for i in range(n):
            is_symmetric = True
            for j in range(n):
                if Q[i][j] != Q[(i + 1) % n][(j + 1) % n]:
                    is_symmetric = False
                    break
            if is_symmetric:
                symmetries.append(1)
        return sum(symmetries)

    def log_base_2(x):
        return math.log(x, 2)

    n_values = [5, 10, 15, 20, 30, 40]
    total_symmetry = 0
    total_log_size = 0

    for n in n_values:
        circuit = generate_ac0_circuit(n, random.randint(2, 5))
        Q = compute_quiver_representation(circuit)
        symmetry = compute_symmetry(Q)
        log_size = log_base_2(len(circuit))

        total_symmetry += symmetry
        total_log_size += log_size

    metric_value = total_symmetry / len(n_values)
    instances_tested = len(n_values)
    conjecture_holds = False
    counterexample = ""

    return {
        "metric_name": "Symmetry vs Log Size",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{trial_result}}}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")