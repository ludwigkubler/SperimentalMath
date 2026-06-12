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
    
    def generate_random_graph(n):
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    adj_matrix[i][j] = 1
                    adj_matrix[j][i] = 1
        return adj_matrix
    
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(n):
            if all(matrix[j][i] == 0 for j in range(m)):
                continue
            rank += 1
            for j in range(i + 1, n):
                if matrix[j][i] != 0:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] -= factor * matrix[i][k]
        return rank
    
    def communication_complexity_rank_variance(n):
        # Placeholder function; actual implementation needed
        return random.randint(1, n)
    
    n = 40
    adj_matrix = generate_random_graph(n)
    rank_A = matrix_rank(adj_matrix)
    comm_rank_var_n = communication_complexity_rank_variance(n)
    
    return {
        "metric_name": "Rank",
        "metric_value": rank_A,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rank_A <= comm_rank_var_n,
        "counterexample": "" if rank_A <= comm_rank_var_n else f"Graph with n={n}, R(A)={rank_A} > CommRankVar(n)={comm_rank_var_n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        r = run_trial(seed)
        print(f"TRIAL: {r}")
        results.append(r)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")