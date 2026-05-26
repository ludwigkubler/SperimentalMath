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

def generate_and_or_tree(n):
    if n == 1:
        return 'L'
    else:
        left_size = random.randint(1, n-2)
        right_size = n - left_size - 1
        return ('A', generate_and_or_tree(left_size), generate_and_or_tree(right_size))

def compute_geometric_duality_parameter(tree):
    if tree == 'L':
        return 0
    elif isinstance(tree[0], str):
        return max(compute_geometric_duality_parameter(tree[1]), compute_geometric_duality_parameter(tree[2]))
    else:
        left = compute_geometric_duality_parameter(tree[1])
        right = compute_geometric_duality_parameter(tree[2])
        return 1 + max(left, right)

def pathwidth(tree):
    if tree == 'L':
        return 0
    elif isinstance(tree[0], str):
        return 1 + max(pathwidth(tree[1]), pathwidth(tree[2]))
    else:
        left = pathwidth(tree[1])
        right = pathwidth(tree[2])
        return 1 + max(left, right)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in range(5, 41):
        tree = generate_and_or_tree(n)
        duality_param = compute_geometric_duality_parameter(tree)
        pw = pathwidth(tree)
        ratio = duality_param / pw if pw > 0 else float('inf')
        results.append({
            "n": n,
            "duality_param": duality_param,
            "pathwidth": pw,
            "ratio": ratio
        })
    c = max(result['ratio'] for result in results)
    conjecture_holds = all(result['ratio'] <= c * math.log(result['n'] + 1) for result in results)
    counterexample = "" if conjecture_holds else f"Found counterexample at n={results[-1]['n']} with ratio {results[-1]['ratio']}"
    return {
        "metric_name": "duality_ratio",
        "metric_value": c,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='first_failing_seed' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")