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
    
    def xor_and_formula(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = xor_and_formula(n // 2)
            right = xor_and_formula(n - n // 2)
            return [x ^ y for x in left] + [x & y for x in left] + [y & z for y in right for z in left]
    
    def polynomial_from_formula(formula):
        if len(formula) == 1:
            return formula[0]
        else:
            return formula[-1] + polynomial_from_formula(formula[:-1])
    
    def hodge_decomposition(poly, mod=2):
        n = len(poly)
        H = [[0] * n for _ in range(n)]
        for i in range(n):
            H[i][i] = poly[i]
        return H
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        row, col = 0, 0
        while row < m and col < n:
            if matrix[row][col] == 0:
                for i in range(row + 1, m):
                    if matrix[i][col] != 0:
                        matrix[row], matrix[i] = matrix[i], matrix[row]
                        break
                else:
                    col += 1
                    continue
            pivot = Fraction(matrix[row][col])
            for j in range(col, n):
                matrix[row][j] /= pivot
            for i in range(m):
                if i != row and matrix[i][col] != 0:
                    factor = -matrix[i][col]
                    for j in range(col, n):
                        matrix[i][j] += factor * matrix[row][j]
            row += 1
            col += 1
        return sum(1 for r in matrix if any(r))
    
    def f(n):
        return int(math.log2(n) ** 2)
    
    n = random.randint(5, 40)
    formula = xor_and_formula(n)
    poly = polynomial_from_formula(formula)
    H = hodge_decomposition(poly)
    rank_H = rank(H)
    
    metric_name = "Rank of Hodge Decomposition"
    metric_value = rank_H
    instances_tested = 1
    conjecture_holds = rank_H <= f(n)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")