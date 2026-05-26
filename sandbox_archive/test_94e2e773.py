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
    
    def gaussian_elimination(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda x: abs(matrix[x][i]))
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        r = 0
        for i in range(m):
            if any(matrix[i]):
                r += 1
        return r
    
    def tropicalize(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            for j in range(n):
                matrix[i][j] = max(0, matrix[i][j])
        return matrix
    
    def dpll_width(formula):
        if not formula:
            return 1
        if isinstance(formula, str):
            return 1
        if isinstance(formula, list):
            if formula[0] == 'OR':
                return max(dpll_width(subformula) for subformula in formula[1:])
            elif formula[0] == 'AND':
                return sum(dpll_width(subformula) for subformula in formula[1:])
    
    def generate_kerdock_code(n):
        code = [[random.choice([0, 1]) for _ in range(n)] for _ in range(2**n)]
        return gaussian_elimination(code)
    
    n = random.randint(5, 40)
    kerdock_code = generate_kerdock_code(n)
    rank_kerdock = rank(kerdock_code)
    tropicalized_kerdock = tropicalize(kerdock_code)
    rank_tropicalized = rank(tropicalized_kerdock)
    
    cnf_formula = ['AND'] + [[random.choice(['OR', 'AND'])] + random.sample(range(n), 2) for _ in range(2**n - 1)]
    width_cnf = dpll_width(cnf_formula)
    
    if rank_tropicalized == 0:
        return {
            "metric_name": "rank_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = rank_tropicalized / (2 ** rank_kerdock)
    std_dev = math.sqrt(0.5 * n)  # Simplified for demonstration
    lower_bound = math.log2(width_cnf) - 3 * std_dev
    
    return {
        "metric_name": "rank_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": 0.9 <= ratio <= 1.1 and ratio >= lower_bound,
        "counterexample": "" if 0.9 <= ratio <= 1.1 and ratio >= lower_bound else f"Ratio {ratio} outside bounds [0.9, 1.1] or below {lower_bound}"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if 0.9 <= r <= 1.1 and r >= math.log2(width_cnf) - 3 * std_dev) / len(results)
    
    if all(r is not None for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        elif support_fraction > 0:
            print(f"RESULT: FALSIFIED counterexample=\"not enough support\" first_failing_seed={seeds[results.index(min(results))]}")
        else:
            print(f"RESULT: INCONCLUSIVE not enough support")
    else:
        print("RESULT: INCONCLUSIVE missing data")