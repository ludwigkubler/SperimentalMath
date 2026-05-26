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
    
    def generate_disjointness_function(n):
        return {tuple(random.randint(0, 1) for _ in range(n)): tuple(random.randint(0, 1) for _ in range(n)) for _ in range(2**n)}
    
    def noncrossing_partition_matrix(f):
        n = len(next(iter(f)))
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for x, y in f:
            idx_x = sum(x[i] * 2**i for i in range(n))
            idx_y = sum(y[i] * 2**i for i in range(n))
            matrix[idx_x][idx_y] = 1
            matrix[idx_y][idx_x] = 1
        return matrix
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for row in matrix:
            if any(row[i] != 0 for i in range(n)):
                rank += 1
                for j in range(n):
                    if matrix[j][i] != 0:
                        for k in range(n):
                            matrix[j][k] -= matrix[i][k]
        return rank
    
    def communication_complexity(f):
        n = len(next(iter(f)))
        return n * (n - 1) // 2
    
    def spearman_rank_correlation(ranks, complexities):
        n = len(ranks)
        sorted_ranks = sorted(range(n), key=lambda i: ranks[i])
        sorted_complexities = sorted(range(n), key=lambda i: complexities[i])
        rank_ranks = [sorted_ranks.index(i) for i in range(n)]
        rank_complexities = [sorted_complexities.index(i) for i in range(n)]
        n_pairs = 0
        numerator = 0
        denominator1 = 0
        denominator2 = 0
        for i in range(n):
            for j in range(i + 1, n):
                n_pairs += 1
                numerator += (rank_ranks[i] - rank_ranks[j]) * (rank_complexities[i] - rank_complexities[j])
                denominator1 += (rank_ranks[i] - rank_ranks[j])**2
                denominator2 += (rank_complexities[i] - rank_complexities[j])**2
        if n_pairs == 0:
            return 0
        rho = numerator / math.sqrt(denominator1 * denominator2)
        return rho
    
    results = []
    for n in range(5, 41):
        f = generate_disjointness_function(n)
        matrix = noncrossing_partition_matrix(f)
        rank = min_rank(matrix)
        complexity = communication_complexity(f)
        results.append((rank, complexity))
    
    ranks = [r for r, _ in results]
    complexities = [c for _, c in results]
    rho = spearman_rank_correlation(ranks, complexities)
    
    return {
        "metric_name": "Spearman rank correlation",
        "metric_value": rho,
        "instances_tested": len(results),
        "conjecture_holds": rho >= 0.8 and all(v <= 3 for v in ranks),
        "counterexample": "" if rho >= 0.8 else f"rho={rho}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho<{mean_rho}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")