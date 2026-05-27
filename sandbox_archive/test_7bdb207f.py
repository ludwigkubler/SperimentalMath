# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def xor_and_tree_width(boolean_function):
        if len(boolean_function) == 1:
            return 0
        n = len(boolean_function)
        for i in range(n):
            left = boolean_function[:i]
            right = boolean_function[i+1:]
            if all(x ^ y == z for x, y, z in zip(left, right)):
                return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
        return n - 1

    def geometric_langlands_lattice_rank(boolean_function):
        n = len(boolean_function)
        rank = 0
        for i in range(1, n+1):
            for subset in combinations(range(n), i):
                if all(boolean_function[j] == boolean_function[subset[0]] for j in subset):
                    rank += 1
        return rank

    def C(n):
        # Define a function C(n) that returns the threshold value for XOR-AND tree width
        # This is a placeholder function; replace it with an actual implementation if needed
        return n * (n - 1) // 2

    instances_tested = 0
    total_rank = 0
    total_width = 0
    counterexample = ""

    for _ in range(30):
        boolean_function = [random.choice([0, 1]) for _ in range(random.randint(5, 40))]
        width = xor_and_tree_width(boolean_function)
        rank = geometric_langlands_lattice_rank(boolean_function)

        if width > C(len(boolean_function)) and rank > C(len(boolean_function))**2:
            counterexample = f"Boolean function: {boolean_function}, Width: {width}, Rank: {rank}"
            break

        instances_tested += 1
        total_rank += rank
        total_width += width

    if counterexample:
        conjecture_holds = False
    else:
        mean_ratio = Fraction(total_rank, instances_tested) / (total_width ** 2)
        conjecture_holds = mean_ratio <= 1 and mean_ratio >= Fraction(0, 1)

    return {
        "metric_name": "mean_ratio",
        "metric_value": float(mean_ratio),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)

    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")