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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k * n):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses):
        n = max(abs(c) for c in set(sum(clauses, [])))
        polynomial = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            i, j = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                polynomial[i][j] += 1
            elif clause[0] < 0 and clause[1] < 0:
                polynomial[-i][-j] += 1
        return polynomial
    
    def noncommutative_crossed_product(poly):
        n = len(poly)
        product = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                for k in range(1, n + 1):
                    product[i][j] += poly[i][k] * poly[k][j]
        return product
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[j][i] != 0 for j in range(i, n)):
                rank += 1
                for j in range(n):
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def bp_readtwice_circuit_threshold(k, n):
        # Simplified approximation for demonstration
        return k * math.log2(n)
    
    n = random.randint(5, 40)
    k = random.randint(1, n // 2)
    instance = generate_kcnf(n, k)
    polynomial = clause_indicator_polynomial(instance)
    crossed_product = noncommutative_crossed_product(polynomial)
    rank = min_rank(crossed_product)
    threshold = bp_readtwice_circuit_threshold(k, n)
    
    if rank > threshold:
        return {
            "metric_name": "Rank vs DPLL Heig",
            "metric_value": rank - threshold,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "rank is greater than threshold"
        }
    
    return {
        "metric_name": "Rank vs DPLL Heig",
        "metric_value": rank - threshold,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    total_rank_diffs = sum(r["metric_value"] for r in results if r["conjecture_holds"])
    num_supporting_seeds = sum(1 for r in results if r["conjecture_holds"])
    mean_rank_diff = total_rank_diffs / num_supporting_seeds
    std_rank_diff = math.sqrt(sum((r["metric_value"] - mean_rank_diff) ** 2 for r in results if r["conjecture_holds"]) / (num_supporting_seeds - 1))
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank_diff} std={std_rank_diff} support_fraction=1.0")
    elif num_supporting_seeds >= 24:
        print(f"RESULT: SUPPORTED mean={mean_rank_diff} std={std_rank_diff} support_fraction={num_supporting_seeds / len(results)}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank is greater than threshold' first_failing_seed={first_failing_seed}")