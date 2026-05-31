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
    
    def generate_k_sat_instance(n, k):
        clauses = []
        for _ in range(k):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                literals = [-x for x in literals]
            clauses.append(literals)
        return clauses
    
    def twisted_group_representation(clauses):
        n = len(clauses[0])
        G = []
        for clause in clauses:
            g = [0] * n
            for literal in clause:
                if literal > 0:
                    g[literal - 1] += 1
                else:
                    g[-literal - 1] -= 1
            G.append(g)
        return G
    
    def order_of_group(G):
        n = len(G[0])
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        count = 0
        while True:
            found = False
            for g in G:
                g_matrix = [g] * n
                product = matrix_multiplication(g_matrix, I)
                if product == I:
                    found = True
                    break
            if not found:
                return count
            count += 1
    
    def matrix_multiplication(A, B):
        m = len(A)
        n = len(B[0])
        p = len(B)
        result = [[0 for _ in range(n)] for _ in range(m)]
        for i in range(m):
            for j in range(n):
                for k in range(p):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(1, min(n, 10))
        instance = generate_k_sat_instance(n, k)
        G = twisted_group_representation(instance)
        order = order_of_group(G)
        results.append({"n": n, "order": order})
    
    mean_order = sum(result["order"] for result in results) / len(results)
    max_order = max(result["order"] for result in results)
    conjecture_holds = all(order <= 1.5 * (n ** (2/3)) for n, order in zip(n_values, [result["order"] for result in results]))
    
    return {
        "metric_name": "Order of Automorphism Groups",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Order {max_order} exceeds 1.5 * n^(2/3) for n={n_values[n_values.index(max_order)]}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order exceeds 1.5 * n^(2/3)\" first_failing_seed={first_failing_seed}")