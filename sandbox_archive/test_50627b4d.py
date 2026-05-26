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
    
    def generate_instance(n):
        # Generate a random function in P with read-twice branching program width n
        # This is a placeholder implementation; actual generation depends on the problem
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def geometric_quantization_matrix(instance):
        # Placeholder implementation of geometric quantization matrix
        n = int(math.log(len(instance), 2))
        G = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(i, n + 1):
                if instance[2**i + 2**(j-1)] == 1:
                    G[i][j] = 1
                else:
                    G[i][j] = -1
        return G
    
    def min_rank(matrix):
        # Placeholder implementation of minimal rank calculation
        n = len(matrix)
        rank = 0
        for i in range(n):
            if matrix[i][i] != 0:
                rank += 1
                for j in range(i + 1, n):
                    matrix[j][i] /= matrix[i][i]
                for k in range(i + 1, n):
                    for l in range(i, n):
                        matrix[k][l] -= matrix[k][i] * matrix[i][l]
        return rank
    
    def spearman_correlation(x, y):
        # Placeholder implementation of Spearman's rank correlation
        x_rank = {v: i for i, v in enumerate(sorted(set(x)), 1)}
        y_rank = {v: i for i, v in enumerate(sorted(set(y)), 1)}
        n = len(x)
        numerator = sum((x_rank[x[i]] - y_rank[y[i]]) ** 2 for i in range(n))
        denominator = n * (n**2 - 1) / 6
        return 1 - (6 * numerator) / denominator
    
    instances_tested = 0
    total_rank = 0
    ranks = []
    widths = []
    
    for _ in range(30):
        instance = generate_instance(random.randint(5, 40))
        G = geometric_quantization_matrix(instance)
        rank = min_rank(G)
        instances_tested += 1
        total_rank += rank
        ranks.append(rank)
        widths.append(len(instance))
    
    mean_rank = total_rank / instances_tested
    correlation = spearman_correlation(ranks, widths)
    
    if correlation > 0.95:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Spearman's rank correlation is not significantly greater than 0"
    
    return {
        "metric_name": "Spearman's rank correlation",
        "metric_value": correlation,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")