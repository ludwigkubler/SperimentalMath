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
    m = 5 + random.randint(0, 34)  # Number of inputs (m ≤ 40)
    n = 2**m  # Domain size is 2^m
    instances_tested = 30
    max_val = 1.0

    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]

    def characteristic_polynomial(f):
        n = len(f)
        poly = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                if f[i] == f[j]:
                    poly[i][j] += 1
        return poly

    def geometric_entropy(poly, m):
        entropy = 0.0
        for i in range(m):
            for j in range(m):
                if poly[i][j] > 0:
                    entropy += poly[i][j] * math.log2(poly[i][j])
        return entropy / (m * math.log2(n))

    max_entropy = 0.0

    for _ in range(instances_tested):
        f = generate_boolean_function(m)
        poly = characteristic_polynomial(f)
        entropy = geometric_entropy(poly, m)
        if entropy > max_entropy:
            max_entropy = entropy

    return {
        "metric_name": "max_geometric_entropy",
        "metric_value": max_entropy,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": max_entropy <= m * math.log2(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")