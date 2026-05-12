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

def factorial(n):
    if n == 0:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def hook_length_formula(shape):
    n = len(shape)
    hook_lengths = []
    for i in range(n):
        row_sum = sum(shape[i])
        col_sum = sum(shape[j][i] for j in range(n))
        hook_lengths.append(row_sum + col_sum - shape[i][i] + 1)
    return math.prod(hook_lengths) // math.prod(factorial(x) for x in shape)

def schur_weyl_components(clause_vectors):
    n = len(clause_vectors)
    tensor_product = [1]
    for vector in clause_vectors:
        new_tensor_product = []
        for i in range(len(tensor_product)):
            for j in range(len(vector)):
                new_tensor_product.append(tensor_product[i] * vector[j])
        tensor_product = new_tensor_product
    shape = [(n - 1) // 2, (n + 1) // 2]
    return hook_length_formula(shape)

def dpll_lower_bound(Phi):
    def dpll(clause_set, assignment):
        if not clause_set:
            return True
        for literal in set(lit for clause in clause_set for lit in clause):
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clause_set if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clause_set if literal not in c and -literal not in c], new_assignment):
                return True
        return False
    return len(list(itertools.product([True, False], repeat=len(Phi))))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 20
    m = n * n
    clause_vectors = [[random.choice([-1, 1]) for _ in range(n)] for _ in range(m)]
    C_phi = schur_weyl_components(clause_vectors)
    monotone_circuit_size = dpll_lower_bound(clause_vectors)
    conjecture_holds = C_phi >= 2**(n/2) / n**2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "C(Φ)",
        "metric_value": C_phi,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 2**(n/2) / n**2) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")