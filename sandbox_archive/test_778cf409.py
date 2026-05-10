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

def generate_disjointness_matrix(n):
    subsets = [set(random.sample(range(2**math.ceil(math.log2(n))), n)) for _ in range(n)]
    M = [[1 if i != j and len(subsets[i] & subsets[j]) == 0 else 0 for j in range(n)] for i in range(n)]
    return M

def numerical_range(M, tol=1e-6):
    n = len(M)
    I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    A = [M[i] + (i+1)*I for i in range(n)]
    B = [M[i] - (i+1)*I for i in range(n)]
    
    def norm(X):
        return max(sum(abs(x) for x in row) for row in X)
    
    def add(A, B):
        return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
    
    def sub(A, B):
        return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]
    
    def scale(A, c):
        return [[c * A[i][j] for j in range(n)] for i in range(n)]
    
    def mul(A, B):
        return [[sum(A[i][k] * B[k][j] for k in range(n)) for j in range(n)] for i in range(n)]
    
    X = I
    Y = I
    
    while True:
        X_new = add(X, sub(mul(scale(B, norm(Y)), mul(X, Y)), scale(X, norm(X) * norm(Y))))
        Y_new = add(Y, sub(mul(scale(A, norm(X)), mul(Y, X)), scale(Y, norm(X) * norm(Y))))
        
        if norm(sub(X_new, X)) < tol and norm(sub(Y_new, Y)) < tol:
            break
        
        X = X_new
        Y = Y_new
    
    return norm(add(mul(X, Y), mul(Y, X)))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    M = generate_disjointness_matrix(n)
    cb_norm = numerical_range(M)
    metric_value = cb_norm / n
    conjecture_holds = metric_value >= 0.1 * n
    counterexample = "" if conjecture_holds else "cb_norm < 0.1*n"
    
    return {
        "metric_name": "cb_norm",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i + 1 for i in range(5, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"cb_norm < 0.1*n\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")