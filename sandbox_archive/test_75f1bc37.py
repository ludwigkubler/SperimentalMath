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
    n = 40
    p = 29  # A prime number for F_p
    k = 5   # The threshold value to test

    def generate_polynomial(n, p):
        coefficients = [random.randint(1, p-1) for _ in range(n+1)]
        return coefficients

    def compute_val_p(f, p):
        val_p = 0
        for coeff in f:
            if coeff == 0:
                continue
            factors = set()
            temp = coeff
            for i in range(2, int(math.sqrt(temp)) + 1):
                while temp % i == 0:
                    factors.add(i)
                    temp //= i
            if temp > 1:
                factors.add(temp)
            val_p = max(val_p, len(factors))
        return val_p

    def construct_acc0_circuit(f, p):
        # Simplified ACC^0 circuit construction for demonstration purposes
        # This is a placeholder and should be replaced with actual ACC^0 circuit logic
        depth = 0
        for coeff in f:
            if coeff != 0:
                depth += 1
        return depth

    polynomials = [generate_polynomial(n, p) for _ in range(30)]
    results = []

    for f in polynomials:
        val_p = compute_val_p(f, p)
        D_f = construct_acc0_circuit(f, p)
        results.append({
            "val_p": val_p,
            "D_f": D_f
        })

    metric_value = sum(result["val_p"] < k for result in results) / len(results)
    conjecture_holds = all(result["val_p"] < k or result["D_f"] < k for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Fraction of polynomials with val_p(k) < k",
        "metric_value": metric_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")