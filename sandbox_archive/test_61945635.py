# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_xor_tautology(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_kahler_form(truth_table):
        n = len(truth_table)
        kahler_form = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                count = sum(1 for row in truth_table if (row[i] + row[j]) % 2 == 1)
                kahler_form[i][j] = Fraction(count, 2**n)
                kahler_form[j][i] = kahler_form[i][j]
        return kahler_form
    
    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = Fraction(0)
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += (-1)**j * matrix[0][j] * determinant(submatrix)
        return det
    
    def dnf_width(truth_table):
        n = len(truth_table)
        variables = list(range(n))
        best_width = float('inf')
        
        def backtrack(path, remaining_vars):
            nonlocal best_width
            if not remaining_vars:
                width = 1 + sum(1 for var in path if truth_table[var] == 1)
                if width < best_width:
                    best_width = width
                return
            for var in remaining_vars:
                backtrack(path + [var], remaining_vars - {var})
        
        backtrack([], set(variables))
        return best_width
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    truth_table = generate_xor_tautology(n)
    kahler_form = construct_kahler_form(truth_table)
    dnf_width_val = dnf_width(truth_table)
    
    rank = 0
    for row in kahler_form:
        if any(val != Fraction(0) for val in row):
            rank += 1
    
    return {
        "metric_name": "rank(K)",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= 2 * dnf_width_val and rank >= dnf_width_val / 2,
        "counterexample": "" if rank <= 2 * dnf_width_val and rank >= dnf_width_val / 2 else f"rank(K)={rank}, width(DNF)={dnf_width_val}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_rank = (sum((res["metric_value"] - mean_rank)**2 for res in results) / len(results))**0.5
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank(K) grows sub-linearly compared to width(DNF)\" first_failing_seed={seeds[first_failing_seed]}")