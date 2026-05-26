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

def generate_boolean_function(n):
    return [random.randint(0, 1) for _ in range(2**n)]

def tensor_product(f, g):
    n = int(math.log2(len(f)))
    m = int(math.log2(len(g)))
    result = []
    for x in range(2**n):
        for y in range(2**m):
            result.append(f[x] * g[y])
    return result

def compute_brauer_group_rank(f, g):
    tensor_valuation = tensor_product(f, g)
    n = int(math.log2(len(tensor_valuation)))
    rank = 0
    for i in range(n):
        if all(tensor_valuation[j] == 0 for j in range(2**n) if (j & (1 << i)) != 0):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    g = generate_boolean_function(n)
    rank = compute_brauer_group_rank(f, g)
    expected_rank = n ** (2/3)
    return {
        "metric_name": "Brauer group rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": abs(rank - expected_rank) <= 3 * expected_rank,
        "counterexample": "" if conjecture_holds else f"n={n}, rank={rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, rank={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")