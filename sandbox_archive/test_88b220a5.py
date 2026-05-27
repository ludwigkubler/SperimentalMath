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

def xor_and_tree_width(f):
    if isinstance(f, int):
        return 0
    elif f[0] == 'AND':
        left, right = f[1], f[2]
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    elif f[0] == 'XOR':
        left, right = f[1], f[2]
        return max(xor_and_tree_width(left), xor_and_tree_width(right))
    else:
        raise ValueError("Invalid boolean function")

def characteristic_polynomial(f):
    if isinstance(f, int):
        return [f]
    elif f[0] == 'AND':
        left, right = f[1], f[2]
        poly_left = characteristic_polynomial(left)
        poly_right = characteristic_polynomial(right)
        n = len(poly_left) + len(poly_right) - 1
        result = [0] * (n + 1)
        for i in range(len(poly_left)):
            for j in range(len(poly_right)):
                result[i + j] += poly_left[i] * poly_right[j]
        return result
    elif f[0] == 'XOR':
        left, right = f[1], f[2]
        poly_left = characteristic_polynomial(left)
        poly_right = characteristic_polynomial(right)
        n = max(len(poly_left), len(poly_right))
        result = [0] * (n + 1)
        for i in range(n):
            result[i] += poly_left[i] - poly_right[i]
        return result
    else:
        raise ValueError("Invalid boolean function")

def degree_of_brauer_group_representation(poly):
    n = len(poly) - 1
    if n == 0:
        return 0
    elif n == 1:
        return abs(poly[1])
    else:
        max_degree = 0
        for i in range(2, n + 1):
            coeff = poly[i]
            if coeff != 0:
                degree = math.log2(abs(coeff))
                if degree > max_degree:
                    max_degree = degree
        return int(max_degree)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    width = xor_and_tree_width(f)
    poly = characteristic_polynomial(f)
    degree = degree_of_brauer_group_representation(poly)
    return {
        "metric_name": "Brauer Group Degree",
        "metric_value": degree,
        "instances_tested": 1,
        "conjecture_holds": width >= degree,
        "counterexample": "" if width >= degree else f"Counterexample: XOR-AND tree width {width} < Brauer group degree {degree}"
    }

def generate_random_boolean_function(n):
    if n == 0:
        return random.choice([0, 1])
    elif n == 1:
        return ('XOR', generate_random_boolean_function(random.randint(0, 1)), generate_random_boolean_function(random.randint(0, 1)))
    else:
        op = random.choice(['AND', 'XOR'])
        left = generate_random_boolean_function(n - 1)
        right = generate_random_boolean_function(n - 1)
        return (op, left, right)

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    degrees = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = len(degrees) / len(results)
    mean = sum(degrees) / len(degrees) if degrees else 0
    std = math.sqrt(sum((x - mean)**2 for x in degrees) / len(degrees)) if degrees else 0

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")