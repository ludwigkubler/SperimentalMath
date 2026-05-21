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
        result = 1
        for i in range(len(mu)):
            result *= binomial_coefficient(lam[i] - sum(mu[:i]), mu[i])
        for i in range(1, len(mu)):
            result //= factorial(mu[i])
        for i in range(len(mu)):
            if lam[i] - sum(mu[:i]) < 0:
                return 0
        return result
    
    def irreducible_character(lam, beta):
        n = len(lam)
        result = murnaghan_nakayama(lam, [0]*n, beta)
        for i in range(n):
            if lam[i] > 1:
                result *= math.sqrt((lam[i]-1) * (lam[i]-2))
        return result
    
    def evaluate_formula(formula):
        if isinstance(formula, tuple):
            row_set, col_set, bijection = formula
            return [bijection[col] for col in range(len(col_set))]
        elif isinstance(formula, list):
            left = evaluate_formula(formula[0])
            right = evaluate_formula(formula[1])
            return [left[i] * right[j] for i in range(len(left)) for j in range(len(right))]
        else:
            raise ValueError("Invalid formula structure")
    
    def calculate_specht_support(f, n):
        dim_V_lambda = 1
        alpha_lambda = 0
        for lam in partitions(n):
            dim_V_lambda *= binomial_coefficient(n, sum(lam))
            alpha_lambda += f[lam] * irreducible_character(lam, [0]*n)
        return (dim_V_lambda * alpha_lambda**2)**2 / (dim_V_lambda * alpha_lambda**4)
    
    def partitions(n):
        if n == 0:
            yield []
        for i in range(1, n + 1):
            for p in partitions(n - i):
                yield [i] + p
    
    n_values = [4, 5, 6, 7]
    s_values = [1, 2, 4, 8, 16, 32]
    instances_tested = 0
    total_r = 0.0
    counterexample = ""
    
    for n in n_values:
        for s in s_values:
            for _ in range(30):
                formula = []
                leaves = [random.sample(range(n), random.randint(1, n)) for _ in range(s)]
                weights = [random.random() for _ in range(s)]
                
                def build_formula(leaves, weights):
                    if len(leaves) == 1:
                        return (leaves[0], leaves[0], weights[0])
                    else:
                        mid = len(leaves) // 2
                        left = build_formula(leaves[:mid], weights[:mid])
                        right = build_formula(leaves[mid:], weights[mid:])
                        return [left, right]
                
                formula = build_formula(leaves, weights)
                
                f = {}
                for lam in partitions(n):
                    f[lam] = 0
                for leaf in leaves:
                    row_set, col_set, bijection = leaf
                    if len(row_set) == 1 and len(col_set) == 1:
                        f[()] += weights[row_set[0]]
                
                specht_support = calculate_specht_support(f, n)
                r = specht_support / s
                
                instances_tested += 1
                total_r += r
                
                if r > 1.05:
                    counterexample = f"Formula size {s}, n={n} has |supp_eff| > 1.05·s"
                
                if len(counterexample) > 0:
                    break
            
            if len(counterexample) > 0:
                break
        
        if len(counterexample) > 0:
            break
    
    conjecture_holds = r <= 1 and total_r / instances_tested <= 1 and max(r for _ in range(instances_tested)) <= 1.05
    mean_r = total_r / instances_tested
    
    return {
        "metric_name": "specht_support_ratio",
        "metric_value": mean_r,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")