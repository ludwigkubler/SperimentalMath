# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def partitions(n):
        if n == 0:
            return [[]]
        result = []
        for p in partitions(n-1):
            for i in range(len(p)+1):
                new_p = p[:i] + [p[i]+[n-1]] + p[i+1:]
                if new_p not in result:
                    result.append(new_p)
        return result
    
    def irreducible_character(lam, sigma):
        n = sum(len(part) for part in lam)
        beta = [0] * (n+1)
        for i, part in enumerate(lam):
            beta[i] = len(part)
        beta[n] = 1
        char = 1
        for i in range(n):
            char *= math.factorial(beta[i])
            char //= math.prod(math.factorial(len(group)) for group in sigma if set(range(i+1, n)).issubset(set(group)))
        return char
    
    def specht_coefficient(f, lam):
        alpha = 0
        for sigma in permutations(lam):
            alpha += f(sigma) * irreducible_character(lam, sigma)
        return alpha / math.factorial(sum(len(part) for part in lam))
    
    def permutations(lam):
        if len(lam) == 1:
            return [list(range(len(lam[0])))]
        result = []
        for i, part in enumerate(lam):
            for perm in permutations(lam[:i] + lam[i+1:]):
                result.append([perm[j] if j < i else perm[j-1] for j in range(len(perm))])
        return result
    
    def effective_specht_support(f, lam):
        n = sum(len(part) for part in lam)
        dim_V_lam = math.prod(math.factorial(len(group)) for group in lam)
        numerator = sum(dim_V_lam * specht_coefficient(f, lam) ** 2 for lam in partitions(n))
        denominator = sum(dim_V_lam * specht_coefficient(f, lam) ** 4 for lam in partitions(n))
        return (numerator / denominator) ** 0.5
    
    def generate_formula(n, s):
        if s == 1:
            row_set = random.sample(range(n), n)
            col_set = random.sample(range(n), n)
            bijection = list(range(n))
            return [(row_set, col_set, bijection), random.random()]
        else:
            left = generate_formula(n, s // 2)
            right = generate_formula(n, s - s // 2)
            return (left, right, '⊗')
    
    def evaluate_formula(formula):
        if isinstance(formula, tuple) and formula[2] == '⊗':
            left = evaluate_formula(formula[0])
            right = evaluate_formula(formula[1])
            result = {}
            for i in range(n):
                for j in range(n):
                    row_set_left, col_set_left, bijection_left = left
                    row_set_right, col_set_right, bijection_right = right
                    if i in row_set_left and j in col_set_right:
                        key = tuple(sorted(row_set_left + [i] + col_set_right + [j]))
                        result[key] = left[i][j] * right[bijection_left[j]][bijection_right[i]]
            return result
        else:
            row_set, col_set, bijection = formula
            return {tuple(sorted(row_set + [i] + col_set + [j])): random.random() for i in range(n) for j in range(n)}
    
    n_values = [4, 5, 6, 7]
    s_values = [1, 2, 4, 8, 16, 32]
    results = []
    
    for n in n_values:
        for s in s_values:
            for _ in range(30):
                formula = generate_formula(n, s)
                f = evaluate_formula(formula)
                lam = partitions(n)[random.randint(0, len(partitions(n)) - 1)]
                r = effective_specht_support(f, lam)
                results.append({"metric_name": "effective_specht_support", "metric_value": r, "instances_tested": 1, "conjecture_holds": r <= s, "counterexample": "" if r <= s else f"Formula size {s}, effective support {r}"})
    
    mean_r = sum(result["metric_value"] for result in results) / len(results)
    max_r = max(result["metric_value"] for result in results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {"seed": seed, "mean_r": mean_r, "max_r": max_r, "support_fraction": support_fraction}

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    mean_r = sum(result["mean_r"] for result in results) / len(results)
    max_r = max(result["max_r"] for result in results)
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if support_fraction >= 0.8 and mean_r <= 1 and max_r <= 1.05:
        print(f"RESULT: SUPPORTED mean={mean_r} std=NA support_fraction={support_fraction}")
    elif any(result["max_r"] > 1.05 for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if result["max_r"] > 1.05)
        print(f"RESULT: FALSIFIED counterexample='Formula size exceeds support' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")