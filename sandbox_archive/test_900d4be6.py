# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def generate_permutations(n):
    if n == 0:
        yield []
    else:
        for perm in generate_permutations(n - 1):
            for i in range(n):
                yield perm[:i] + [n - 1] + perm[i:]

def calculate_major_index(sigma):
    descents = [i for i in range(len(sigma) - 1) if sigma[i] > sigma[i + 1]]
    return sum(descents)

def run_trial(seed):
    random.seed(seed)
    n = random.choice([3, 4, 5, 6, 7, 8, 9, 10])
    M = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    T_M = []
    for sigma in generate_permutations(n):
        compatible = True
        for i in range(n):
            if M[i][sigma[i]] != 1:
                compatible = False
                break
        if compatible:
            T_M.append(sigma)
    if len(T_M) < 2:
        return {
            "metric_name": "R_2(M)",
            "metric_value": 0.0,
            "instances_tested": len(T_M),
            "conjecture_holds": True,
            "counterexample": ""
        }
    perm_2 = 0
    det_2 = 0
    for sigma in T_M:
        maj = calculate_major_index(sigma)
        perm_2 += 2 ** maj
        sign = (-1) ** sum(1 for i in range(len(sigma) - 1) if sigma[i] > sigma[i + 1])
        det_2 += sign * (2 ** maj)
    R_2 = perm_2 / max(1, abs(det_2))
    bound = math.sqrt(len(T_M)) / (2 * n)
    conjecture_holds = R_2 >= bound
    counterexample = "" if conjecture_holds else f"R_2(M) = {R_2} < sqrt(|T_M|)/(2n) = {bound}"
    return {
        "metric_name": "R_2(M)",
        "metric_value": R_2,
        "instances_tested": len(T_M),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    metric_values = []
    conjecture_holds_all = True
    counterexample = ""
    first_failing_seed = None
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        metric_values.append(result["metric_value"])
        if not result["conjecture_holds"]:
            conjecture_holds_all = False
            counterexample = result["counterexample"]
            first_failing_seed = seed
            break
    if not conjecture_holds_all:
        print(f'RESULT: FALSIFIED counterexample="{counterexample}" first_failing_seed={first_failing_seed}')
    else:
        mean = sum(metric_values) / len(metric_values)
        std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
        support_fraction = sum(1 for x in metric_values if x >= 0) / len(metric_values)
        print(f'RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}')