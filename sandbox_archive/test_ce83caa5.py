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
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(A[i][j]) > abs(A[i_max][j]):
                    i_max = i
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank:
                    factor = -A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] += factor * A[rank][k]
            rank += 1
        return rank

    def monomial_ideal_rank(n, k):
        # Generate a random k-CLIQUE instance
        vertices = list(range(n))
        edges = set()
        for _ in range(k):
            u = random.choice(vertices)
            v = random.choice(vertices)
            if u != v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        
        # Construct the associated monomial ideal
        I = []
        for edge in edges:
            i, j = edge
            monomial = [0] * n
            monomial[i] = 1
            monomial[j] = 1
            I.append(monomial)
        
        # Compute the tropical curve rank
        A = [[max(I[i][j], I[j][i]) for j in range(n)] for i in range(n)]
        return gaussian_elimination(A)

    n_min, n_max = 5, 40
    instances_tested = 0
    total_rank = 0

    for n in range(n_min, n_max + 1):
        rank = monomial_ideal_rank(n, k)
        if rank is None:
            return {
                "metric_name": "tropical_curve_rank",
                "metric_value": None,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        total_rank += rank
        instances_tested += 1

    mean_rank = Fraction(total_rank, instances_tested)
    f_n = math.log(n_max) * n_max**2
    if mean_rank < f_n:
        return {
            "metric_name": "tropical_curve_rank",
            "metric_value": float(mean_rank),
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"mean rank {mean_rank} < {f_n}"
        }
    else:
        return {
            "metric_name": "tropical_curve_rank",
            "metric_value": float(mean_rank),
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results):
        mean_rank = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_rank)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean rank < {math.log(n_max) * n_max**2}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")