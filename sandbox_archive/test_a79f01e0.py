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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def minterms(f, n):
        terms = []
        for i in range(2**n):
            if f[i] == 1:
                term = [int(x) for x in format(i, f'0{n}b')]
                terms.append(term)
        return terms
    
    def monomial_ideals(mints):
        ideals = set()
        n = len(mints[0])
        for mint in mints:
            ideal = tuple(sorted([i for i, bit in enumerate(mint) if bit == 1]))
            ideals.add(ideal)
        return ideals
    
    def dynkin_diagram(n):
        if n == 2:  # A_1
            return {'vertices': [0], 'edges': []}
        elif n == 3:  # A_2
            return {'vertices': [0, 1], 'edges': [(0, 1)]}
        elif n == 4:  # A_3
            return {'vertices': [0, 1, 2], 'edges': [(0, 1), (1, 2)]}
        elif n == 5:  # A_4
            return {'vertices': [0, 1, 2, 3], 'edges': [(0, 1), (1, 2), (2, 3)]}
        else:
            raise ValueError("Unsupported number of variables for Dynkin diagram")
    
    def spearman_rank_correlation(x, y):
        n = len(x)
        x_ranks = {x[i]: i + 1 for i in range(n)}
        y_ranks = {y[i]: i + 1 for i in range(n)}
        
        sum_differences_squared = sum((x_ranks[x[i]] - y_ranks[y[i]]) ** 2 for i in range(n))
        rho_numerator = n * sum_differences_squared
        rho_denominator = (n * (n**2 - 1)) * (1 - (6 * sum_differences_squared) / (n**3 - n))
        
        return 1 - (rho_numerator / rho_denominator)
    
    n_values = [5, 10, 15, 20, 30, 40]
    x_values = []
    y_values = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        mints = minterms(f, n)
        ideals = monomial_ideals(mints)
        dynkin = dynkin_diagram(n)
        
        x_values.append(len(ideals))
        y_values.append(len(dynkin['vertices']))
    
    rho = spearman_rank_correlation(x_values, y_values)
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(n_values),
        "conjecture_holds": rho >= 0.7,
        "counterexample": "" if rho >= 0.7 else f"Spearman rank correlation < 0.7: {rho}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rho = sum(r['metric_value'] for r in results) / len(results)
    std_rho = math.sqrt(sum((r['metric_value'] - mean_rho) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation < 0.7\" first_failing_seed={first_failing_seed}")