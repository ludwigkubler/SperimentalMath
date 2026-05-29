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
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + random.randint(0, n - i - 1)
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(i + 1, n):
                factor = A[j][i] / pivot
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def symmetric_bilinear_form(X):
        n = len(X)
        B = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                B[i][j] = sum(x1 & x2 for x1, x2 in zip(X[i], X[j]))
                B[j][i] = B[i][j]
        return B
    
    def communication_complexity(X):
        n = len(X)
        m = 2 ** n
        C = [[0] * m for _ in range(m)]
        for i in range(m):
            for j in range(m):
                x1, x2 = [int(b) for b in f"{i:0{n}b}"], [int(b) for b in f"{j:0{n}b}"]
                C[i][j] = sum(x1[k] ^ x2[k] for k in range(n))
        return max(max(row) for row in C)
    
    def log_squared(n):
        if n <= 0:
            return 0
        return math.log(n, 2) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    complexities = []
    
    for n in n_values:
        X = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        B = symmetric_bilinear_form(X)
        rank = gaussian_elimination(B)
        rank *= len([x for x in X if any(x)])
        ranks.append(rank)
        complexities.append(communication_complexity(X))
    
    if not ranks or not complexities:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": 0.0,
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    def spearman_rank_correlation(ranks, complexities):
        n = len(ranks)
        rank_ranks = {x: i for i, x in enumerate(sorted(set(ranks)), 1)}
        rank_complexities = {x: i for i, x in enumerate(sorted(set(complexities)), 1)}
        sum_diff_squared = sum((rank_ranks[r] - rank_complexities[c]) ** 2 for r, c in zip(ranks, complexities))
        return 1 - (6 * sum_diff_squared) / (n * (n**2 - 1))
    
    rho = spearman_rank_correlation(ranks, complexities)
    c = rho * log_squared(n_values[-1])
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": rho,
        "instances_tested": len(n_values),
        "conjecture_holds": rho > 0.8 and all(rank <= c * log_squared(n) for n, rank in zip(n_values, ranks)),
        "counterexample": "" if rho > 0.8 else f"rho={rho}, c*{n_values[-1]}^2={c*log_squared(n_values[-1])}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")