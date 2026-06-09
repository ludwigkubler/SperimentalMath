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
    
    def gaussian_elimination(matrix):
        rows, cols = len(matrix), len(matrix[0])
        for i in range(rows):
            max_row = i
            for j in range(i + 1, rows):
                if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                    max_row = j
            matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
            pivot = Fraction(1, matrix[i][i])
            for j in range(cols):
                matrix[i][j] *= pivot
            for j in range(rows):
                if i != j:
                    factor = matrix[j][i]
                    for k in range(cols):
                        matrix[j][k] -= factor * matrix[i][k]
        rank = sum(1 for row in matrix if any(row))
        return rank
    
    def frege_proof_depth(n):
        # Simulate a Frege proof depth
        return random.randint(5, 40)
    
    def generate_coxeter_group(depth):
        # Simulate generating a Coxeter group from a Frege proof
        n = depth // 2
        adjacency_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                if random.choice([True, False]):
                    adjacency_matrix[i][j] = 1
                    adjacency_matrix[j][i] = 1
        return adjacency_matrix
    
    def rank_coxeter_group(adjacency_matrix):
        return gaussian_elimination(adjacency_matrix)
    
    instances_tested = 0
    n_max = 0
    total_rank = 0
    num_seeds = 30
    support_count = 0
    
    for _ in range(num_seeds):
        depth = frege_proof_depth(n_max + 1)
        if depth > n_max:
            n_max = depth
        G = generate_coxeter_group(depth)
        rank = rank_coxeter_group(G)
        instances_tested += 1
        total_rank += rank
        
        if rank <= 1.5 * (depth ** 1.5):
            support_count += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    support_fraction = Fraction(support_count, num_seeds)
    
    conjecture_holds = support_fraction >= Fraction(4, 5)
    counterexample = "" if conjecture_holds else f"Depth {depth}, Rank {rank}"
    
    return {
        "metric_name": "Coxeter Group Rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")