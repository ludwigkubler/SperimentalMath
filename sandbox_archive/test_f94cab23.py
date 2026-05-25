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
    
    def generate_boolean_function(X):
        return [random.choice([0, 1]) for _ in range(2**X)]
    
    def matrix_representation(f, X, Y):
        M = [[0] * (2**Y) for _ in range(2**X)]
        for x in range(2**X):
            for y in range(2**Y):
                if f[x] == 1 and f[(x >> y) & 1] == 1:
                    M[x][y] = 1
        return M
    
    def tropical_rank(M):
        rows, cols = len(M), len(M[0])
        rank = 0
        for i in range(rows):
            if any(M[i][j] != 0 for j in range(cols)):
                rank += 1
                for j in range(cols):
                    if M[i][j] != 0:
                        for k in range(rows):
                            M[k][j] = max(M[k][j], M[i][j] + M[k][i])
        return rank
    
    def communication_complexity(M):
        rows, cols = len(M), len(M[0])
        cc = float('inf')
        for i in range(rows):
            if any(M[i][j] != 0 for j in range(cols)):
                cc = min(cc, sum(1 for j in range(cols) if M[i][j] != 0))
        return cc
    
    def run_instance(X, Y):
        f = generate_boolean_function(X)
        M = matrix_representation(f, X, Y)
        tau_G_M = tropical_rank(M)
        CC_DISJ_M = communication_complexity(M)
        return tau_G_M**2 <= CC_DISJ_M
    
    n_tests = 30
    results = [run_instance(random.randint(3, 40), random.randint(3, 40)) for _ in range(n_tests)]
    
    metric_value = sum(results) / len(results)
    conjecture_holds = all(results)
    counterexample = "" if conjecture_holds else "CC_{DISJ}(M) < τ_G(M)^2"
    
    return {
        "metric_name": "Communication Complexity vs Tropical Rank",
        "metric_value": metric_value,
        "instances_tested": n_tests,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 3072) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"CC_{DISJ}(M) < τ_G(M)^2\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")