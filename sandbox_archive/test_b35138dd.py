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
    
    def generate_truth_table(n):
        return [[random.choice([0, 1]) for _ in range(2**n)] for _ in range(2**n)]
    
    def formal_context_order(truth_table):
        n = len(truth_table)
        order = 0
        for i in range(n):
            for j in range(i+1, n):
                if truth_table[i][j] != truth_table[j][i]:
                    order += 1
        return order
    
    def matrix_representation_rank(truth_table):
        n = len(truth_table)
        A = [[truth_table[i][j] for j in range(n)] for i in range(n)]
        rank = 0
        for i in range(n):
            if all(A[j][i] == 0 for j in range(i)):
                continue
            pivot_row = next(j for j in range(i, n) if A[j][i] != 0)
            A[i], A[pivot_row] = A[pivot_row], A[i]
            rank += 1
            for j in range(n):
                if j == i:
                    continue
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        return rank
    
    def log2(x):
        if x <= 0:
            return None
        count = 0
        while x > 1:
            x /= 2
            count += 1
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ratio = 0
    instances_tested = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        if n > n_max:
            n_max = n
        for _ in range(5):  # 5 instances per size for statistical signal
            truth_table = generate_truth_table(n)
            order = formal_context_order(truth_table)
            rank = matrix_representation_rank(truth_table)
            if rank == 0:
                continue
            ratio = Fraction(order, rank)
            total_ratio += ratio
            instances_tested += 1
            if ratio > log2(n):
                conjecture_holds = False
                counterexample = f"n={n}, Order: {order}, Rank: {rank}, Ratio: {ratio}, Log2(n): {log2(n)}"
    
    mean_ratio = total_ratio / instances_tested if instances_tested else None
    std_ratio = (sum((Fraction(order, rank) - mean_ratio)**2 for order, rank in zip(formal_context_order(truth_table), matrix_representation_rank(truth_table))) / instances_tested)**0.5 if instances_tested else None
    
    return {
        "metric_name": "Ratio of Formal Context Order to Matrix Representation Rank",
        "metric_value": float(mean_ratio) if mean_ratio is not None else None,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = (sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_data")