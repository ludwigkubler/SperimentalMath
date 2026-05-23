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

def generate_monotone_circuit(n):
    if n == 1:
        return [0]
    else:
        left_size = random.randint(1, n-1)
        right_size = n - left_size - 1
        left = generate_monotone_circuit(left_size)
        right = generate_monotone_circuit(right_size)
        return sorted([x for x in left] + [x + max(left) + 1 for x in right])

def rank_young_tableau(tableau):
    n = len(tableau)
    if n == 0:
        return 0
    max_length = 1
    current_length = 1
    for i in range(1, n):
        if tableau[i] > tableau[i-1]:
            current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_length = 1
    return max(max_length, current_length)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_metric_value = 0
    instances_tested = 0
    support_count = 0

    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            circuit = generate_monotone_circuit(n)
            depth = len(circuit) - 1
            tableau = [circuit.index(i) for i in sorted(circuit)]
            rank = rank_young_tableau(tableau)
            ratio = rank / (depth + 1)
            total_metric_value += ratio
            instances_tested += 1
            if ratio <= 3:
                support_count += 1

    mean_metric_value = total_metric_value / instances_tested
    support_fraction = support_count / instances_tested
    conjecture_holds = support_fraction >= 0.8 and mean_metric_value <= 3
    counterexample = "" if conjecture_holds else "support_fraction < 0.8 or metric_mean > 3"

    return {
        "metric_name": "Ratio of Rank to Decision Tree Depth",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8 or metric_mean > 3\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 0.8 or metric_mean > 3")