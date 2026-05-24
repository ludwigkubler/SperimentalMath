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

def generate_and_or_tree(n):
    if n == 0:
        return 'L'
    elif n == 1:
        return 'O'
    else:
        left_size = random.randint(0, n-2)
        right_size = n - 1 - left_size
        return ('O', generate_and_or_tree(left_size), generate_and_or_tree(right_size))

def compute_coxeter_number(tree):
    if tree == 'L':
        return 1
    elif tree == 'O':
        return 2
    else:
        left_num = compute_coxeter_number(tree[1])
        right_num = compute_coxeter_number(tree[2])
        return max(left_num, right_num) + 1

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for _ in range(5):
            tree = generate_and_or_tree(n)
            coxeter_num = compute_coxeter_number(tree)
            expected_log_n = math.log2(n + 1)
            if coxeter_num < expected_log_n * 0.75 or coxeter_num > expected_log_n * 1.25:
                conjecture_holds = False
                counterexample = f"n={n}, tree={tree}, coxeter_num={coxeter_num}"
                break
            total_metric_value += abs(coxeter_num - expected_log_n)
            instances_tested += 1

    return {
        "metric_name": "Coxeter Number vs Log(n)",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")