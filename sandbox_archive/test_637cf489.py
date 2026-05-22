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
    
    n = 10  # Starting with n=10 to avoid trivial cases
    k = 3   # Example value for k in k-CLIQUE problem
    
    if n < 5 or k <= 0:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "n_min=5, k>0 required"
        }
    
    # Generate a random graph with n vertices
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = 0
    
    # Find all subspaces S of dimension at least d
    def find_subspaces(A, d):
        subspaces = []
        for i in range(2**n):
            subspace = [j for j in range(n) if (i >> j) & 1]
            if len(subspace) >= d:
                subspaces.append(subspace)
        return subspaces
    
    subspaces = find_subspaces(A, k)
    
    # Compute R(S) for each subspace S
    def rank(subspace, A):
        m = len(subspace)
        B = [[A[i][j] for j in subspace] for i in subspace]
        r = 0
        for i in range(m):
            if B[i][i] == 0:
                for j in range(i+1, m):
                    if B[j][i] != 0:
                        B[i], B[j] = B[j], B[i]
                        break
                    if j == m-1:
                        return r
            pivot = B[i][i]
            for j in range(m):
                B[i][j] /= pivot
            for j in range(i+1, m):
                factor = B[j][i]
                for l in range(m):
                    B[j][l] -= factor * B[i][l]
            r += 1
        return r
    
    min_rank = math.inf
    for subspace in subspaces:
        min_rank = min(min_rank, rank(subspace, A))
    
    # Check if the conjecture holds
    conjecture_holds = min_rank >= n**2 / k
    counterexample = "" if conjecture_holds else "n={}, k={}, min_rank={}".format(n, k, min_rank)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": len(subspaces),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample='{}' first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")