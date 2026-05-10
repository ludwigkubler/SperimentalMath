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

def fast_walsh_hadamard_transform(a):
    n = len(a)
    while n > 1:
        for i in range(n // 2):
            for j in range(i, i + n // 2):
                t = a[j] ^ a[j + n // 2]
                a[j] ^= t
                a[j + n // 2] ^= t
        n //= 2
    return a

def fourier_coefficients(f, n):
    a = [f(i) for i in range(1 << n)]
    return fast_walsh_hadamard_transform(a)

def indicator_function(x, n):
    return all((x >> i) & 1 == (i % 3 != 0) for i in range(n))

def dpll_resolution_length(f, n):
    def memoized_clause_resolution(clauses, assignment):
        if not clauses:
            return 0
        clause = random.choice(clauses)
        literal = random.choice(clause)
        new_assignment = assignment[:]
        new_assignment[literal] = True
        new_clauses = [c for c in clauses if not any(l in c for l in new_assignment)]
        return 1 + memoized_clause_resolution(new_clauses, new_assignment)

    initial_assignment = [False] * n
    return memoized_clause_resolution(f, initial_assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    instances_tested = 30
    total_length = 0
    total_coeff_sum = 0

    for _ in range(instances_tested):
        f = lambda x: indicator_function(x, n)
        coefficients = fourier_coefficients(f, n)
        coeff_sum = sum(abs(c) for c in coefficients)
        length = dpll_resolution_length(f, n)

        total_length += length
        total_coeff_sum += coeff_sum

    metric_value = total_length / instances_tested
    conjecture_holds = total_length >= total_coeff_sum
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "resolution_proof_length",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]]
    if not seeds:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = primes[:30]

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")