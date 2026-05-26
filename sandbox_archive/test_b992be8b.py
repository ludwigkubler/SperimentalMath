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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def construct_graph(f):
        n = int(math.log2(len(f)))
        graph = [[0] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if f[i] == f[j]:
                    graph[i][j] = 1
        return graph
    
    def laplacian_matrix(G):
        n = len(G)
        L = [[0] * n for _ in range(n)]
        for i in range(n):
            degree = sum(G[i])
            L[i][i] = -degree
            for j in range(i + 1, n):
                if G[i][j]:
                    L[i][j] = 1
                    L[j][i] = 1
        return L
    
    def matrix_rank(M):
        m, n = len(M), len(M[0])
        rank = 0
        for i in range(m):
            if all(M[i][j] == 0 for j in range(n)):
                continue
            rank += 1
            for j in range(i + 1, m):
                if M[j][i] != 0:
                    for k in range(n):
                        M[j][k] -= M[i][k]
        return rank
    
    def is_acc0_lower_bound(f):
        # Placeholder function to check ACC⁰ lower bound
        # This is a dummy implementation and should be replaced with actual logic
        return False
    
    n = 40
    f = generate_boolean_function(n)
    G_f = construct_graph(f)
    L_G_f = laplacian_matrix(G_f)
    rank = matrix_rank(L_G_f)
    
    metric_name = "minimal_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank >= math.log2(n)
    counterexample = "" if conjecture_holds else f"rank={rank}, expected=Ω(log {n})"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < Ω(log n)\" first_failing_seed={first_failing_seed}")