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

def xor(a, b):
    return a ^ b

def inner_product(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def generate_anf_polynomial(n, d):
    terms = [random.choice([0, 1]) for _ in range(2**n)]
    coefficients = [random.choice([-1, 1])]
    for i in range(d):
        new_terms = [xor(x, y) for x, y in zip(terms, terms[1:])]
        coefficients.append(random.choice([-1, 1]))
        terms.extend(new_terms)
    return coefficients

def generate_xor_function(n, d=None):
    if d is None:
        d = random.randint(2, 4)
    polynomial = generate_anf_polynomial(n, d)
    return lambda x: polynomial[0] + sum(coeff * inner_product(polynomial[i+1:], x) for i in range(len(polynomial)-1))

def walsh_hadamard_transform(f, n):
    N = 2**n
    result = [[0]*N for _ in range(N)]
    for u in range(N):
        for v in range(N):
            sum_val = 0
            for x in range(N):
                sum_val += f(x) * (-1)**(inner_product(bin(u)[2:].zfill(n), bin(v)[2:].zfill(n)))
            result[u][v] = sum_val / math.sqrt(N)
    return result

def lehmer_pair_density(walsh_coeffs):
    nonzero_coeffs = [abs(coeff) for coeff in walsh_coeffs if coeff != 0]
    nonzero_coeffs.sort()
    n = len(nonzero_coeffs)
    count = sum((nonzero_coeffs[i+1] - nonzero_coeffs[i]) < (nonzero_coeffs[i+1] + nonzero_coeffs[i]) / (8 * math.log2(1 + i)) for i in range(n-1))
    return count / n

def discrepancy(M_f):
    N = len(M_f)
    max_val = 0
    for u in range(N):
        for v in range(N):
            val = abs(inner_product(M_f[u], M_f[v]))
            if val > max_val:
                max_val = val
    return N / (2 * max_val)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [6, 8, 11, 14]
    c = 1/16
    results = []
    
    for n in n_values:
        instances_tested = 0
        conjecture_holds = True
        counterexample = ""
        
        # Random ANF d∈{2,3,4}
        for _ in range(5):
            f = generate_xor_function(n)
            M_f = walsh_hadamard_transform(f, n)
            L_f = lehmer_pair_density([abs(coeff) for coeff in M_f if coeff != 0])
            disc_M_f = discrepancy(M_f)
            instances_tested += 1
            if disc_M_f * (1 + L_f) < c * 2**(-n/2):
                conjecture_holds = False
                counterexample = "Random ANF d∈{2,3,4}"
        
        # Inner-product
        for _ in range(5):
            f = lambda x: inner_product(x, [1]*n)
            M_f = walsh_hadamard_transform(f, n)
            L_f = lehmer_pair_density([abs(coeff) for coeff in M_f if coeff != 0])
            disc_M_f = discrepancy(M_f)
            instances_tested += 1
            if disc_M_f * (1 + L_f) < c * 2**(-n/2):
                conjecture_holds = False
                counterexample = "Inner-product"
        
        # Equality
        for _ in range(5):
            f = lambda x: int(x[0] == x[1])
            M_f = walsh_hadamard_transform(f, n)
            L_f = lehmer_pair_density([abs(coeff) for coeff in M_f if coeff != 0])
            disc_M_f = discrepancy(M_f)
            instances_tested += 1
            if disc_M_f * (1 + L_f) < c * 2**(-n/2):
                conjecture_holds = False
                counterexample = "Equality"
        
        # Threshold
        for _ in range(5):
            f = lambda x: int(sum(x) >= n//2)
            M_f = walsh_hadamard_transform(f, n)
            L_f = lehmer_pair_density([abs(coeff) for coeff in M_f if coeff != 0])
            disc_M_f = discrepancy(M_f)
            instances_tested += 1
            if disc_M_f * (1 + L_f) < c * 2**(-n/2):
                conjecture_holds = False
                counterexample = "Threshold"
        
        # Clustered-spectrum
        for _ in range(5):
            f = lambda x: sum(x)
            M_f = walsh_hadamard_transform(f, n)
            L_f = lehmer_pair_density([abs(coeff) for coeff in M_f if coeff != 0])
            disc_M_f = discrepancy(M_f)
            instances_tested += 1
            if disc_M_f * (1 + L_f) < c * 2**(-n/2):
                conjecture_holds = False
                counterexample = "Clustered-spectrum"
        
        results.append({
            "metric_name": "disc_M_f * (1 + L_f)",
            "metric_value": disc_M_f * (1 + L_f),
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    mean_metric = sum(result["metric_value"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["metric_value"] - mean_metric)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "results": results,
        "mean_metric": mean_metric,
        "std_metric": std_metric,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_metric = sum(result["mean_metric"] for result in results) / len(results)
    std_metric = math.sqrt(sum((result["mean_metric"] - mean_metric)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")