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
    
    def generate_cnf(n):
        clauses = []
        for i in range(1, n + 1):
            clause = [random.randint(-i, -1), random.randint(i, n)]
            clauses.append(clause)
        return clauses
    
    def resolution(cnf):
        clauses = cnf[:]
        while True:
            new_clauses = set()
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    p, q = clauses[i][0], clauses[j][0]
                    if -p == q:
                        new_clause = [c for c in clauses[i] if c != p] + [c for c in clauses[j] if c != q]
                        new_clauses.add(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.extend(new_clauses)
        return len(clauses)
    
    def symplectic_form(cnf):
        n = len(cnf[0])
        M = [[0] * (2 * n) for _ in range(2 * n)]
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    i, j = lit - 1, lit + n - 1
                else:
                    i, j = -lit - 1, -lit - 1
                M[i][j] += 1
        rank = 0
        for row in M:
            if any(row):
                pivot_col = next(j for j in range(2 * n) if row[j])
                for other_row in M:
                    if other_row[pivot_col]:
                        factor = Fraction(other_row[pivot_col], row[pivot_col])
                        for k in range(2 * n):
                            other_row[k] -= factor * row[k]
                rank += 1
        return rank
    
    def spearman_correlation(ranks, weights):
        if len(ranks) != len(weights):
            raise ValueError("ranks and weights must have the same length")
        n = len(ranks)
        sorted_ranks = sorted(range(n), key=lambda i: ranks[i])
        sorted_weights = [weights[sorted_ranks[i]] for i in range(n)]
        rank_diffs = [(i - j) ** 2 for i, j in zip(sorted_ranks, range(n))]
        weight_diffs = [(w1 - w2) ** 2 for w1, w2 in zip(sorted_weights, weights)]
        numerator = sum(rank_diffs * weight_diffs)
        denominator = (sum(rank_diffs) * sum(weight_diffs)) / n
        return numerator / denominator
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    w_phi = resolution(cnf)
    r_phi = symplectic_form(cnf)
    
    if w_phi == 0:
        return {
            "metric_name": "Spearman Correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "resolution_width_zero"
        }
    
    ranks = [-r_phi, math.log2(w_phi)]
    weights = [1 / w_phi, 1 / w_phi]
    correlation = spearman_correlation(ranks, weights)
    
    return {
        "metric_name": "Spearman Correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation > 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"spearman_correlation\" first_failing_seed={first_failing_seed}")