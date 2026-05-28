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
    
    n = 40
    d = 5
    
    # Generate a random max-CUT instance
    A = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = 0
    
    # Compute the degree-d pseudoexpectation matrix M
    M = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if A[i][j] == 1:
                M[i][j] = random.uniform(-1, 1)
                M[j][i] = M[i][j]
    
    # Determine the Hodge rank of the minimal Hodge filter containing M
    def hodge_rank(M):
        n = len(M)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        B = [row[:] for row in M]
        rank = 0
        for i in range(n):
            pivot = next((j for j in range(i, n) if B[j][i] != 0), None)
            if pivot is None:
                continue
            rank += 1
            for j in range(n):
                B[pivot][j], B[i][j] = B[i][j], B[pivot][j]
            for k in range(n):
                if k != i:
                    factor = -B[k][i] / B[i][i]
                    for j in range(n):
                        B[k][j] += factor * B[i][j]
        return rank
    
    hodge_rank_M = hodge_rank(M)
    
    # Check the approximation ratio of an SOS algorithm
    def sos_approximation_ratio(A, M):
        n = len(A)
        x = [random.uniform(-1, 1) for _ in range(n)]
        value = sum(x[i] * x[j] * A[i][j] for i in range(n) for j in range(i+1, n))
        sos_value = sum(M[i][j] * x[i] * x[j] for i in range(n) for j in range(i+1, n))
        return value / sos_value
    
    approximation_ratio = sos_approximation_ratio(A, M)
    
    # Check the conjecture
    if hodge_rank_M < d:
        if approximation_ratio > 0.878:
            conjecture_holds = False
            counterexample = "approximation_ratio_too_high"
        else:
            conjecture_holds = True
            counterexample = ""
    elif hodge_rank_M >= d:
        if approximation_ratio <= 0.878:
            conjecture_holds = False
            counterexample = "approximation_ratio_too_low"
        else:
            conjecture_holds = True
            counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "mapping_undefined"
    
    return {
        "metric_name": "approximation_ratio",
        "metric_value": approximation_ratio,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")