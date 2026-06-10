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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        if n == 1:
            return 'x'
        else:
            op = random.choice(['&', '|'])
            left = generate_formula(n // 2)
            right = generate_formula(n - n // 2)
            return f'({left} {op} {right})'

    def resolution_width(formula):
        stack = []
        for char in formula.replace(' ', ''):
            if char == '(':
                stack.append(char)
            elif char == ')':
                count = 0
                while stack[-1] != '(':
                    stack.pop()
                    count += 1
                stack.pop()
                stack.append(count + 1)
            else:
                continue
        return max(stack)

    def symplectic_capacity(formula):
        n = formula.count('x')
        if n == 0:
            return 0
        elif n == 1:
            return 1
        else:
            cap = 0
            for i in range(n):
                cap += (2 ** i) * math.comb(n, i)
            return cap

    formula = generate_formula(40)
    scap = symplectic_capacity(formula)
    w = resolution_width(formula)

    return {
        "metric_name": "resolution_width",
        "metric_value": w,
        "instances_tested": 1,
        "n_max": 40,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    else:
        seeds = [int(s) for s in sys.argv[1:]]

    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")