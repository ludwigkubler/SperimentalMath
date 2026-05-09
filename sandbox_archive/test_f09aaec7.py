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

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_primes(n):
    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def fast_walsh_hadamard_transform(arr):
    N = len(arr)
    if N <= 1:
        return arr
    even = fast_walsh_hadamard_transform(arr[::2])
    odd = fast_walsh_hadamard_transform(arr[1::2])
    result = [0] * N
    for k in range(N // 2):
        result[k] = even[k] + odd[k]
        result[k + N // 2] = even[k] - odd[k]
    return result

def dpll(cnf, assignment={}):
    if not cnf:
        return True
    literals = set()
    for clause in cnf:
        literals.update(clause)
    literal = next(iter(literals))
    positive_literal = literal > 0
    new_assignment = assignment.copy()
    new_assignment[literal] = positive_literal
    if dpll(cnf, new_assignment):
        return True
    new_assignment[literal] = not positive_literal
    if dpll(cnf, new_assignment):
        return True
    return False

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = []
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        if len(set(clause)) == len(clause) and len(clause) > 0:
            cnf.append(clause)
    def evaluate_formula(formula, assignment):
        return all(any(lit in assignment and assignment[lit] == (lit > 0) for lit in clause) for clause in formula)
    def fourier_coefficient(cnf, subset):
        n = len(subset)
        N = 2 ** n
        coefficients = [0] * N
        for i in range(N):
            assignment = {subset[j]: (i >> j) & 1 for j in range(n)}
            if evaluate_formula(cnf, assignment):
                coefficients[i] += 1
        return sum(abs(coefficients[i]) for i in range(N))
    subset_size = random.randint(1, n)
    subsets = [set(random.sample(range(1, n + 1), subset_size)) for _ in range(10)]
    fourier_sum = sum(fourier_coefficient(cnf, subset) for subset in subsets)
    dpll_tree_size = 0
    while not dpll(cnf):
        dpll_tree_size += 1
    return {
        "metric_name": "DPLL Tree Size",
        "metric_value": dpll_tree_size,
        "instances_tested": len(subsets),
        "conjecture_holds": fourier_sum > 0 and dpll_tree_size <= 1 / fourier_sum * 2,
        "counterexample": "" if fourier_sum > 0 else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or generate_primes(30)
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE mapping_undefined")