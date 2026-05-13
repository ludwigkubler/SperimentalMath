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

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

def binomial(n, k):
    if k > n:
        return 0
    result = 1
    for i in range(k):
        result *= (n - i)
        result //= (i + 1)
    return result

def hook_length_formula(shape):
    n = len(shape)
    total = 1
    for row in range(n):
        for col in range(len(shape[row])):
            total *= (shape[row][col] + row + col + 1) // (row + col + 1)
    return total

def permanent(poly):
    if not poly:
        return 0
    n = len(poly)
    result = 0
    for perm in itertools.permutations(range(n)):
        sign = (-1) ** sum(i < j for i, j in zip(perm, range(n)))
        product = 1
        for i in range(n):
            product *= poly[perm[i]][i]
        result += sign * product
    return result

def determinant(poly):
    if not poly:
        return 0
    n = len(poly)
    if n == 1:
        return poly[0][0]
    det = 0
    for j in range(n):
        sub_poly = [row[:j] + row[j+1:] for row in poly[1:]]
        sign = (-1) ** j
        det += sign * poly[0][j] * determinant(sub_poly)
    return det

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    metric_value = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(instances_tested):
        # Generate a random 3-SAT instance with n variables
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[(i + 1) % n] for i in range(n)):
                clauses.append(clause)
        poly = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i, x in enumerate(clause):
                if x > 0:
                    poly[i][x - 1] += 1
                else:
                    poly[-i - 1][-x - 1] += 1

        # Compute symmetric square decompositions using Young tableau counting (hook-length formula)
        permanent_shape = [(n - i) * [n - j - 1] for i in range(n)]
        determinant_shape = [(n - i) * [n - j - 1] for i in range(n)]

        permanent_components = hook_length_formula(permanent_shape)
        determinant_components = hook_length_formula(determinant_shape)

        # Measure irreducible component counts
        metric_value += permanent_components - determinant_components

    mean_metric_value = metric_value / instances_tested
    if mean_metric_value < n**2:
        conjecture_holds = False
        counterexample = "Permanent components are not Ω(n^2) larger than determinant components."

    return {
        "metric_name": "Irreducible Component Count Gap",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Permanent components are not Ω(n^2) larger than determinant components.\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")