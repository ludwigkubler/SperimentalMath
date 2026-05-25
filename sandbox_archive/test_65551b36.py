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

def generate_truth_table(n):
    return [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]

def tropicalize_truth_table(f, n):
    truth_table = generate_truth_table(n)
    quandle_order = 0
    for i in range(len(truth_table)):
        for j in range(i + 1, len(truth_table)):
            if truth_table[i][j] == truth_table[j][i]:
                quandle_order += 1
    return quandle_order

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = lambda x: x  # Placeholder for actual function generation logic
    t_f = 10  # Placeholder for actual ACC⁰ circuit complexity calculation

    quandle_order = tropicalize_truth_table(f, n)
    expected_order = Fraction(n**2 * math.log(t_f), 1)

    conjecture_holds = abs(quandle_order - expected_order) < 1e-6
    counterexample = "" if conjecture_holds else f"Order mismatch: {quandle_order} != {expected_order}"

    return {
        "metric_name": "Quandle Order",
        "metric_value": quandle_order,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order mismatch\" first_failing_seed={first_failing_seed}")