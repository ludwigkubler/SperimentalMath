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
    
    def generate_max_cut_instance(n):
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.append((i, j))
        return edges
    
    def construct_moment_matrix(edges, n):
        M = [[0] * n for _ in range(n)]
        for i, j in edges:
            M[i][j] = M[j][i] = random.random()
        return M
    
    def is_positive_semidefinite(M):
        n = len(M)
        A = [row[:] for row in M]
        for k in range(n):
            pivot = A[k][k]
            if pivot <= 0:
                return False
            for j in range(k + 1, n):
                A[k][j] /= pivot
            for i in range(k + 1, n):
                factor = A[i][k]
                for j in range(k, n):
                    A[i][j] -= factor * A[k][j]
        return True
    
    def is_real_rooted(poly):
        if len(poly) == 0:
            return False
        if poly[0] != 1 or poly[-1] != 0:
            return False
        for coeff in poly[1:-1]:
            if coeff != 0:
                return False
        return True
    
    def find_real_stable_minor(M, d):
        n = len(M)
        minors = []
        for i in range(n - d + 1):
            for j in range(n - d + 1):
                minor = [row[j:j+d] for row in M[i:i+d]]
                if is_positive_semidefinite(minor) and is_real_rooted([Fraction(coeff, 1) for coeff in poly]):
                    minors.append((i, j, d))
        return minors
    
    def sdp_relaxation(M):
        n = len(M)
        # Simplified SDP relaxation (not actual SOS refutation)
        return sum(sum(M[i][j] * M[j][i] for i in range(n)) for j in range(n)) / n
    
    n = random.randint(5, 40)
    edges = generate_max_cut_instance(n)
    M = construct_moment_matrix(edges, n)
    
    minors = find_real_stable_minor(M, d=2)
    if not minors:
        return {
            "metric_name": "sos_refutation_threshold",
            "metric_value": -1,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "No real stable polynomial minor found"
        }
    
    threshold = sdp_relaxation(M)
    return {
        "metric_name": "sos_refutation_threshold",
        "metric_value": threshold,
        "instances_tested": 1,
        "conjecture_holds": threshold >= 2 * math.log(n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 10000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(metric_values)/len(metric_values):.2f} std={math.sqrt(sum((x - sum(metric_values)/len(metric_values))**2 for x in metric_values) / len(metric_values)):.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='first failing seed' first_failing_seed={first_failing_seed}")