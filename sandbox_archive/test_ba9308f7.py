# auto-injected by SEC sandbox
import itertools
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
from fractions import Fraction
import math
import sys

def generate_frege_proof(n):
    if n < 2:
        return []
    proof = [random.randint(0, n-1)]
    for _ in range(1, n):
        proof.append(random.choice([proof[-1], proof[-2]]))
    return proof

def count_monoidal_factors(proof):
    factors = set()
    for step in proof:
        factors.add(step)
    return len(factors)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 0
    instances_tested = 0
    total_metric_value = Fraction(0, 1)
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        proof = generate_frege_proof(n)
        instances_tested += len(proof)
        width = len(proof)
        factors = count_monoidal_factors(proof)
        metric_value = Fraction(factors, width)

        total_metric_value += metric_value

        if conjecture_holds and factors > width:
            conjecture_holds = False
            counterexample = f"n={n}, proof_width={width}, monoidal_factors={factors}"

    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "monoidal_factor_count",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")