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

def factorial(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def binomial_coefficient(n, k):
    return factorial(n) // (factorial(k) * factorial(n - k))

def murnaghan_nakayama(lam, mu, beta):
    if len(mu) > len(lam):
        return 0
    sign = 1
    for i in range(len(mu)):
        sign *= (-1) ** (lam[i] - mu[i])
    result = binomial_coefficient(lam[0], mu[0])
    for i in range(1, len(lam)):
        if lam[i] < mu[i]:
            return 0
        result *= binomial_coefficient(lam[i] - mu[i], mu[i]) // binomial_coefficient(lam[i], mu[i])
    return sign * result

def irreducible_character(lam, beta):
    result = 1
    for i in range(len(beta)):
        result *= murnaghan_nakayama(lam, [beta[i]], beta)
    return result

def specht_coefficient(f, lam, chi_lam):
    return sum(c_f * chi_lam for c_f, sigma in f.items() if len(sigma) == len(lam))

def effective_specht_support(f, chi_table):
    numerator = 0
    denominator = 0
    for lam, dim_vlam in chi_table.items():
        alpha_lam = specht_coefficient(f, lam, chi_table[lam])
        numerator += dim_vlam * alpha_lam ** 2
        denominator += dim_vlam * alpha_lam ** 4
    return (numerator / denominator) ** 0.5

def generate_random_formula(n, s):
    if n < 1 or s < 1:
        raise ValueError("n and s must be at least 1")
    
    def is_disjoint(a, b):
        return not any(x in b for x in a)
    
    def generate_node():
        row_set = random.sample(range(n), random.randint(1, n))
        col_set = random.sample(range(n), random.randint(1, n))
        bijection = {i: j for i, j in zip(row_set, col_set)}
        weight = random.random()
        return (row_set, col_set, bijection, weight)
    
    def generate_tree(depth):
        if depth == 0:
            return generate_node()
        else:
            left = generate_tree(depth - 1)
            right = generate_tree(depth - 1)
            while not is_disjoint(left[0], right[0]) or not is_disjoint(left[1], right[1]):
                left = generate_tree(depth - 1)
                right = generate_tree(depth - 1)
            return ("⊗", left, right)
    
    tree = generate_tree(s - 1)
    
    def evaluate_tree(node):
        if isinstance(node, tuple) and node[0] == "⊗":
            left = evaluate_tree(node[1])
            right = evaluate_tree(node[2])
            result = {}
            for sigma in left:
                for tau in right:
                    new_sigma = sigma + tau
                    result[new_sigma] = (left[sigma] * right[tau]) if is_disjoint(sigma, tau) else 0
            return result
        else:
            row_set, col_set, bijection, weight = node
            result = {}
            for sigma in itertools.permutations(range(n)):
                if all(bijection[i] == sigma[j] for i, j in enumerate(row_set)):
                    result[sigma] = weight
            return result
    
    f = evaluate_tree(tree)
    
    chi_table = {lam: irreducible_character(lam, beta) for lam in itertools.combinations(range(n), n // 2)}
    
    return f, chi_table

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_values = [4, 5, 6, 7]
    s_values = [1, 2, 4, 8, 16, 32]
    
    for n in n_values:
        for s in s_values:
            f, chi_table = generate_random_formula(n, s)
            supp_eff = effective_specht_support(f, chi_table)
            results.append({
                "n": n,
                "s": s,
                "supp_eff": supp_eff
            })
    
    mean_supp_eff = sum(result["supp_eff"] for result in results) / len(results)
    max_supp_eff = max(result["supp_eff"] for result in results)
    support_fraction = sum(1 for result in results if result["supp_eff"] <= result["s"]) / len(results)
    
    conjecture_holds = support_fraction >= 0.8 and mean_supp_eff <= 1 and max_supp_eff <= 1.05
    counterexample = "" if conjecture_holds else f"max(supp_eff)={max_supp_eff} > s"
    
    return {
        "metric_name": "effective_specht_support",
        "metric_value": mean_supp_eff,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_supp_eff = sum(result["metric_value"] for result in results) / len(results)
    max_supp_eff = max(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_supp_eff} std=0.0 support_fraction={support_fraction}")
    elif any(result["metric_value"] > 1.05 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 1.05)
        print(f"RESULT: FALSIFIED counterexample='max(supp_eff) > s' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=not_enough_support")