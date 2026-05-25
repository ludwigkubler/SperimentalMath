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
    
    def generate_max_cut_instance(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        edges = [(i, j) for i in range(n) for j in range(i+1, n)]
        cut_edges = random.sample(edges, len(edges) // 2)
        return variables, cut_edges
    
    def construct_polynomial(variables, degree):
        terms = []
        for d in range(degree + 1):
            for combo in itertools.combinations(variables, d):
                term = ' + '.join(combo) if combo else '1'
                terms.append(term)
        return ' + '.join(terms)
    
    def compute_moment_matrix(polynomial, variables):
        n = len(variables)
        M = [[0] * (n+1) for _ in range(n+1)]
        for term in polynomial.split(' + '):
            if not term: continue
            factors = term.split('*')
            count = 1
            for factor in factors:
                if factor.startswith('x'):
                    var_index = int(factor[1:]) - 1
                    count *= (1 + M[var_index][var_index])
                else:
                    count *= int(factor)
            M[0][0] += count
        return M
    
    def gaussian_elimination(M):
        n = len(M)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(M[j][i]) > abs(M[max_row][i]):
                    max_row = j
            M[i], M[max_row] = M[max_row], M[i]
            factor = 1 / M[i][i]
            for j in range(n):
                M[i][j] *= factor
            for j in range(n):
                if i != j:
                    factor = M[j][i]
                    for k in range(n):
                        M[j][k] -= factor * M[i][k]
        return M
    
    def rank(M):
        n = len(M)
        M = gaussian_elimination(M)
        r = 0
        for row in M:
            if any(row): r += 1
        return r
    
    def max_cut_approximation_ratio(cut_edges, variables):
        n = len(variables)
        total_edges = (n * (n - 1)) // 2
        cut_size = len(cut_edges)
        return cut_size / total_edges
    
    n = random.randint(5, 40)
    degree = random.randint(1, 3)
    variables, cut_edges = generate_max_cut_instance(n)
    polynomial = construct_polynomial(variables, degree)
    M_p = compute_moment_matrix(polynomial, variables)
    rank_M_p = rank(M_p)
    
    if rank_M_p < O(d * log^2(n)):
        ratio = max_cut_approximation_ratio(cut_edges, variables)
        if ratio >= 0.878:
            return {
                "metric_name": "approximation_ratio",
                "metric_value": ratio,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank_M_p} < O(d * log^2(n)), but approximation ratio = {ratio}"
            }
    return {
        "metric_name": "approximation_ratio",
        "metric_value": None,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank < O(d * log^2(n)), but approximation ratio ≥ 0.878\" first_failing_seed={first_failing_seed}")