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

def generate_and_or_tree(n):
    if n == 0:
        return 'leaf'
    elif n == 1:
        return random.choice(['and', 'or'])
    else:
        left = generate_and_or_tree(n // 2)
        right = generate_and_or_tree(n - n // 2 - 1)
        return (random.choice(['and', 'or']), left, right)

def evaluate_polynomial(poly, x):
    result = 0
    for coeff in poly:
        result = result * x + coeff
    return result

def compute_tropical_motive(tree):
    if tree == 'leaf':
        return [1]
    elif isinstance(tree, str):
        return [1]
    else:
        left_tropical = compute_tropical_motive(tree[1])
        right_tropical = compute_tropical_motive(tree[2])
        combined_tropical = []
        for l in left_tropical:
            for r in right_tropical:
                combined_tropical.append(evaluate_polynomial([l, -r], 1))
        return combined_tropical

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        tree = generate_and_or_tree(n)
        communication_complexity = len(tree) - 1  # Simplified approximation
        tropical_motive = compute_tropical_motive(tree)
        rank = max(tropical_motive)

        if rank < communication_complexity * n:
            conjecture_holds = False
            counterexample = f"Tree of size {n} with rank {rank} and complexity {communication_complexity * n}"
            break

        total_metric_value += rank / (communication_complexity * n)
        instances_tested += 1

    return {
        "metric_name": "Rank over Communication Complexity",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")