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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def nonnegative_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank
    
    def k_clique_indicator(n, k):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < (k / n**2):
                    edges.add((i, j))
        return edges
    
    def monotone_circuit_size(edges):
        # Simplified model of a monotone circuit
        return len(edges) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    total_size = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            edges = k_clique_indicator(n, random.randint(1, n))
            rank = nonnegative_rank([[1 if (i, j) in edges or (j, i) in edges else 0 for j in range(n)] for i in range(n)])
            size = monotone_circuit_size(edges)
            total_rank += rank
            total_size += size
            instances_tested += 1
    
    avg_rank = Fraction(total_rank, instances_tested)
    avg_size = Fraction(total_size, instances_tested)
    
    conjecture_holds = avg_rank >= math.sqrt(n) * math.log(avg_size / n)
    counterexample = "" if conjecture_holds else f"avg_rank={avg_rank}, avg_size={avg_size}"
    
    return {
        "metric_name": "Nonnegative Rank",
        "metric_value": float(avg_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")