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
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def min_local_cohomology_rank(V):
        n = len(V)
        A = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if V[i] == V[j]:
                    A[i][j] = 1
                    A[j][i] = 1
        rank = 0
        for row in gaussian_elimination(A):
            if any(row):
                rank += 1
        return rank
    
    def resolution_proof_width(phi):
        # Placeholder for actual computation of resolution proof width
        # This is a dummy implementation for demonstration purposes
        return len(phi)
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_h1 = 0
    total_w = 0
    
    for n in n_values:
        for _ in range(5):
            phi = [''.join(random.choice('01') for _ in range(n)) for _ in range(n)]
            V = [tuple(int(bit) for bit in clause) for clause in phi]
            h1 = min_local_cohomology_rank(V)
            w = resolution_proof_width(phi)
            total_h1 += h1
            total_w += w
            instances_tested += 1
    
    mean_h1 = total_h1 / instances_tested
    mean_w = total_w / instances_tested
    correlation_coefficient = (instances_tested * sum(h1*w for h1, w in zip([mean_h1]*instances_tested, [mean_w]*instances_tested)) - 
                               sum(h1 for h1 in [mean_h1]*instances_tested) * sum(w for w in [mean_w]*instances_tested)) / \
                              math.sqrt((instances_tested * sum(h1**2 for h1 in [mean_h1]*instances_tested) - (sum(h1 for h1 in [mean_h1]*instances_tested))**2) *
                                        (instances_tested * sum(w**2 for w in [mean_w]*instances_tested) - (sum(w for w in [mean_w]*instances_tested))**2))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation_coefficient)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.6)
        print("RESULT: FALSIFIED counterexample={} first_failing_seed={}".format(first_failing_seed, first_failing_seed))
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")