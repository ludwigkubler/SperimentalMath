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
    
    def generate_dnf(n):
        terms = []
        for _ in range(2 ** n):
            term = 0
            for j in range(n):
                if random.choice([True, False]):
                    term |= (1 << j)
            terms.append(term)
        return terms
    
    def moment_matrix(dnf):
        m = len(dnf)
        n = int(math.log2(m))
        M = [[0] * (n + 1) for _ in range(n + 1)]
        for term in dnf:
            for i in range(n + 1):
                if term & (1 << i):
                    M[i][i] += 1
        return M
    
    def tropicalize(M):
        n = len(M)
        T = [[-math.inf] * n for _ in range(n)]
        for i in range(n):
            T[i][i] = M[i][i]
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    T[i][j] = max(T[i][j], min(T[i][k], T[k][j]))
        return T
    
    def minimal_rank(T):
        n = len(T)
        rank = 0
        for _ in range(n):
            pivot = None
            for i in range(rank, n):
                if T[i][rank] != -math.inf:
                    pivot = i
                    break
            if pivot is None:
                return rank
            for j in range(n):
                T[pivot][j], T[rank][j] = T[rank][j], T[pivot][j]
            for i in range(n):
                if i != rank:
                    factor = -T[i][rank] / T[rank][rank]
                    for j in range(n):
                        T[i][j] += factor * T[rank][j]
            rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        dnf = generate_dnf(n)
        M = moment_matrix(dnf)
        T = tropicalize(M)
        rank = minimal_rank(T)
        total_rank += rank
        instances_tested += len(dnf)
    
    mean_minimal_rank = Fraction(total_rank, instances_tested)
    n_mean = Fraction(sum(n_values), len(n_values))
    
    if mean_minimal_rank < n_mean ** (1/4) * n_mean:
        return {
            "metric_name": "Minimal Rank of Tropicalized Moment Matrices",
            "metric_value": float(mean_minimal_rank),
            "instances_tested": instances_tested,
            "conjecture_holds": False,
            "counterexample": f"mean_minimal_rank < n^(1/4) * mean_n for n = {n_values}"
        }
    else:
        return {
            "metric_name": "Minimal Rank of Tropicalized Moment Matrices",
            "metric_value": float(mean_minimal_rank),
            "instances_tested": instances_tested,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_minimal_rank = sum(res["metric_value"] for res in results) / len(results)
    n_mean = Fraction(sum([5, 10, 15, 20, 30, 40]), 6)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_minimal_rank} std=NA support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_minimal_rank} std=NA support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mean_minimal_rank < n^(1/4) * mean_n' first_failing_seed={first_failing_seed}")