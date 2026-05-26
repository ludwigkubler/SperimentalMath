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
    
    def noncrossing_partition_matrix(f):
        n = len(next(iter(f.keys())))
        matrix = [[0] * n for _ in range(n)]
        for x, y in f:
            if len(x) != n or len(y) != n:
                continue
            for i in range(n):
                for j in range(i + 1, n):
                    if (x[i] == '1' and x[j] == '0') and (y[i] == '0' and y[j] == '1'):
                        matrix[i][j] = 1
        return matrix
    
    def min_rank(matrix):
        n = len(matrix)
        rank = 0
        for i in range(n):
            if any(matrix[i]):
                pivot_row = next((r for r, row in enumerate(matrix) if any(row)), None)
                if pivot_row is not None:
                    matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
                    rank += 1
                    for j in range(n):
                        if i != j and matrix[j][i]:
                            factor = Fraction(-matrix[j][i], matrix[i][i])
                            for k in range(n):
                                matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def communication_complexity(f):
        n = len(next(iter(f.keys())))
        # Using a simple deterministic protocol
        return 2 * n - 1
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = {}
        for _ in range(30):
            x = ''.join(random.choice('01') for _ in range(n))
            y = ''.join(random.choice('01') for _ in range(n))
            f[(x, y)] = random.randint(0, 1)
        
        matrix = noncrossing_partition_matrix(f)
        rank = min_rank(matrix)
        comm_complexity = communication_complexity(f)
        
        results.append({
            "n": n,
            "rank": rank,
            "comm_complexity": comm_complexity
        })
    
    if not results:
        return {
            "metric_name": "Spearman Rank Correlation",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    ranks = [result["rank"] for result in results]
    comm_complexities = [result["comm_complexity"] for result in results]
    
    def spearman_rank_correlation(ranks, comm_complexities):
        n = len(ranks)
        rank_ranks = {x: i + 1 for i, x in enumerate(sorted(set(ranks)))}
        rank_comm_ranks = {y: i + 1 for i, y in enumerate(sorted(set(comm_complexities)))}
        
        sum_diff_squares = sum((rank_ranks[r] - rank_comm_ranks[c]) ** 2 for r, c in zip(ranks, comm_complexities))
        return 1 - (6 * sum_diff_squares) / (n * (n**2 - 1))
    
    correlation = spearman_rank_correlation(ranks, comm_complexities)
    
    return {
        "metric_name": "Spearman Rank Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.8 and all(v <= 3 for v in ranks),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = len([r for r in results if r["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Spearman rank correlation < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")