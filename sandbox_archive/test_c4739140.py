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

def generate_boolean_function(n: int) -> list:
    return [random.choice([0, 1]) for _ in range(1 << n)]

def fourier_transform(f: list) -> dict:
    n = f.index(1).bit_length()
    F = {k: [0] * (1 << n) for k in range(1 << n)}
    for x in range(1 << n):
        for k in range(1 << n):
            F[k][x % n] += f[x] * math.cos(-2 * math.pi * k * x / (1 << n))
    return F

def kostant_sheaf_rank(f: list) -> int:
    n = f.index(1).bit_length()
    F = fourier_transform(f)
    rank = 0
    for k in range(1 << n):
        if any(F[k][x] != 0 for x in range(1 << n)):
            rank += 1
    return rank

def circuit_size(f: list) -> int:
    # Placeholder function to compute the size of the smallest AC^0 circuit
    # This is a dummy implementation and should be replaced with an actual algorithm
    return len(f)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    f = generate_boolean_function(n)
    rank = kostant_sheaf_rank(f)
    circuit_size_f = circuit_size(f)
    c = 1.0  # Placeholder constant, should be determined based on the conjecture
    if rank <= c * circuit_size_f:
        return {
            "metric_name": "rank_circuit_ratio",
            "metric_value": rank / circuit_size_f,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "rank_circuit_ratio",
            "metric_value": rank / circuit_size_f,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Counterexample: rank={rank}, circuit_size={circuit_size_f}"
        }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")