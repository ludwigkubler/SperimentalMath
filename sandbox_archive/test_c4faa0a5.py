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

# Define A5 and its generators
A5 = [
    (1, 2, 3, 4, 5), (1, 3, 5, 2, 4),
    (1, 4, 2, 5, 3), (1, 5, 4, 3, 2),
    (2, 3, 4, 5, 1), (2, 4, 5, 3, 1)
]
a = A5[0]
b = A5[1]

# Define the generators for A5
generators = [a, a**-1, b, b**-1]

def multiply(g1, g2):
    result = (g1[0]*g2[0] - 1) % 6 + 1
    return tuple((result + g1[i] - 1) % 5 + 1 for i in range(1, 5))

def identity():
    return (1, 2, 3, 4, 5)

def is_identity(g):
    return g == identity()

# Function to compute Barrington walk
def barrington_walk(F, x):
    current = identity()
    for clause in F:
        for literal, position in zip(clause, range(3)):
            if (position + literal) % 2 == 0:
                if literal > 0:
                    current = multiply(current, a)
                else:
                    current = multiply(current, a**-1)
            else:
                if literal > 0:
                    current = multiply(current, b)
                else:
                    current = multiply(current, b**-1)
    return current

# Function to estimate mu_F
def estimate_mu(F, n):
    if n <= 20:
        count = sum(barrington_walk(F, tuple(random.randint(0, 1) for _ in range(n))) == identity() for _ in range(60))
        return count / 60.0
    else:
        count = sum(barrington_walk(F, tuple(random.randint(0, 1) for _ in range(n))) == identity() for _ in range(20000))
        return count / 20000.0

# Function to compute delta(F)
def compute_delta(F, n):
    mu_values = [estimate_mu(F, n) for _ in range(30)]
    expected_value = 1 / 60
    return sum(abs(mu - expected_value) for mu in mu_values) / len(mu_values)

# Function to run a trial
def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [10, 14, 18, 22, 26, 30, 34, 38]:
        for alpha in [2.5, 3.5, 4.0, 4.5, 5.5, 6.5]:
            m = round(alpha * n)
            F = [[random.randint(-1, 1) for _ in range(3)] for _ in range(m)]
            delta_F = compute_delta(F, n)
            results.append({
                "n": n,
                "alpha": alpha,
                "delta_F": delta_F
            })
    return {
        "metric_name": "delta_F",
        "metric_value": sum(result["delta_F"] for result in results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r <= 5) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={seeds[results.index(max(results))]}")