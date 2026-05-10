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

def generate_gf2_polynomial(n):
    return [random.choice([0, 1]) for _ in range(2**n)]

def matroid_rank(poly):
    n = int(math.log2(len(poly)))
    rank = 0
    basis = []
    for i in range(n):
        if poly[i] == 1:
            basis.append(i)
            rank += 1
            for j in range(i + 1, n):
                if poly[j] == 1 and any((poly[j] & (1 << k)) != 0 for k in basis):
                    poly[j] ^= (1 << i)
    return rank

def acc0_circuit_size(poly):
    n = int(math.log2(len(poly)))
    size = 0
    for i in range(n):
        if poly[i] == 1:
            size += 1
            for j in range(i + 1, n):
                if poly[j] == 1 and any((poly[j] & (1 << k)) != 0 for k in range(i)):
                    size += 1
    return size

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    c = 1.0  # Constant to be adjusted
    instances_tested = 30
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        poly = generate_gf2_polynomial(n)
        rank = matroid_rank(poly)
        size = acc0_circuit_size(poly)
        if size < c * n**(1 + 1/rank):
            conjecture_holds = False
            counterexample = f"Rank {rank}, Size {size}"
            break

    return {
        "metric_name": "acc0_circuit_size",
        "metric_value": acc0_circuit_size(poly),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 8)]  # First 3 prime powers greater than 40

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

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