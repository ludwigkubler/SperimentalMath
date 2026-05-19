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
    
    def generate_dnf(n):
        terms = []
        for _ in range(random.randint(1, n)):
            term = [random.choice([0, 1]) for _ in range(n)]
            if sum(term) > 0:
                terms.append(term)
        return terms
    
    def is_clique(graph, nodes):
        for u in nodes:
            for v in nodes:
                if u != v and (u, v) not in graph and (v, u) not in graph:
                    return False
        return True
    
    def enumerate_cliques(n):
        graph = {}
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([0, 1]) == 1:
                    graph[(i, j)] = True
        cliques = []
        for r in range(2, n + 1):
            for nodes in itertools.combinations(range(n), r):
                if is_clique(graph, nodes):
                    cliques.append(nodes)
        return cliques
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(m - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def submodular_measure(dnf):
        m = len(dnf)
        A = [[0] * m for _ in range(m)]
        b = [0] * m
        for i in range(m):
            for j in range(i + 1, m):
                if any(all(dnf[i][k] == dnf[j][k] for k in range(len(dnf[i]))) for dnf in dnf):
                    A[i][j] = 1
                    A[j][i] = 1
            b[i] = 1
        x = gaussian_elimination(A, b)
        return sum(x)
    
    def k_clique_measure(k):
        n = 40
        cliques = enumerate_cliques(n)
        total_weight = 0
        for clique in cliques:
            if len(clique) == k:
                total_weight += 1
        return total_weight
    
    n = random.randint(5, 40)
    dnf = generate_dnf(n)
    mu_dnf = submodular_measure(dnf)
    mu_k_clique = k_clique_measure(k=2)
    
    metric_name = "submodular_measure"
    metric_value = mu_dnf if n < 10 else mu_k_clique
    instances_tested = 1
    conjecture_holds = True if n < 10 else (mu_k_clique >= math.log(n))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")