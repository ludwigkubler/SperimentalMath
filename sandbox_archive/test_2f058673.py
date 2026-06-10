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

def generate_formula(n):
    if n == 1:
        return 'p'
    else:
        left = generate_formula(random.randint(1, min(n-2, 3)))
        right = generate_formula(n - len(left) - 2)
        return f'({left} ∨ {right})'

def incidence_poset(formula):
    if formula == 'p':
        return {'p'}
    elif '∨' in formula:
        left, right = formula.split(' ∨ ')
        poset_left = incidence_poset(left)
        poset_right = incidence_poset(right)
        return poset_left.union(poset_right).union({f'({left} ∨ {right})'})
    else:
        raise ValueError("Invalid formula")

def ehrhart_semigroup(poset):
    if not poset:
        return 0
    max_steps = 0
    for element in poset:
        steps = len(element.split(' ∨ '))
        if steps > max_steps:
            max_steps = steps
    return max_steps

def resolution_proof_width(formula):
    if formula == 'p':
        return 1
    elif '∨' in formula:
        left, right = formula.split(' ∨ ')
        return max(resolution_proof_width(left), resolution_proof_width(right))
    else:
        raise ValueError("Invalid formula")

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    total_steps = 0
    total_width = 0

    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            formula = generate_formula(n)
            poset = incidence_poset(formula)
            steps = ehrhart_semigroup(poset)
            width = resolution_proof_width(formula)
            total_steps += steps
            total_width += width
            instances_tested += 1

    mean_steps = total_steps / instances_tested
    mean_width = total_width / instances_tested
    correlation_coefficient = (instances_tested * total_steps * total_width - 
                               sum(steps * width for steps, width in zip(range(5, n_max + 1), range(5, n_max + 1)))) / \
                              ((instances_tested * sum(steps**2 for steps in range(5, n_max + 1)) - 
                                (sum(range(5, n_max + 1)) ** 2)) *
                               (instances_tested * sum(width**2 for width in range(5, n_max + 1)) - 
                                (sum(range(5, n_max + 1)) ** 2)))

    mean_abs_diff = abs(mean_steps - mean_width)

    conjecture_holds = correlation_coefficient >= 0.8 and mean_abs_diff <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> mean_abs_diff=<{}>".format(correlation_coefficient, mean_abs_diff)

    return {
        "metric_name": "resolution_proof_width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))