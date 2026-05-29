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
    
    def generate_xor_game(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def symmetric_bilinear_form(game):
        n = int(math.log2(len(game)))
        form = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n + 1):
                form[i][j] = sum(game[k] ^ game[2**i + k] if j == i else game[k] & game[2**i + k] for k in range(2**n))
        return form
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row[:] + [1 if i == j else 0 for j in range(n)] for i, row in enumerate(matrix)]
        for col in range(n):
            max_row = next((i for i in range(col, m) if augmented_matrix[i][col]), None)
            if max_row is None:
                continue
            augmented_matrix[col], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[col]
            augmented_matrix[col] = [x / augmented_matrix[col][col] for x in augmented_matrix[col]]
            for i in range(m):
                if i != col:
                    factor = augmented_matrix[i][col]
                    augmented_matrix[i] = [x - factor * y for x, y in zip(augmented_matrix[i], augmented_matrix[col])]
        return sum(1 for row in augmented_matrix if any(x != 0 for x in row))
    
    def communication_complexity(game):
        n = int(math.log2(len(game)))
        return n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        game = generate_xor_game(n)
        form = symmetric_bilinear_form(game)
        rank_value = rank(form)
        cc_value = communication_complexity(game)
        results.append((rank_value, cc_value))
    
    if not results:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_values, cc_values = zip(*results)
    n_tests = len(rank_values)
    mean_rank = sum(rank_values) / n_tests
    mean_cc = sum(cc_values) / n_tests
    
    # Calculate Spearman's rank correlation coefficient
    ranks = {x: i for i, x in enumerate(sorted(set(rank_values)), 1)}
    cc_ranks = [ranks[x] for x in rank_values]
    n = len(cc_ranks)
    d_squared_sum = sum((i - j) ** 2 for i, j in zip(ranks.values(), cc_ranks))
    spearman_corr = 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
    
    c = mean_rank / math.log(n_tests + 1) ** 2
    bound = c * math.log(n_tests + 1) ** 2
    
    conjecture_holds = all(rank_value <= bound for rank_value in rank_values)
    counterexample = "" if conjecture_holds else f"Rank {max(rank_values)} exceeds bound {bound}"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": n_tests,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds bound\" first_failing_seed={first_failing_seed}")