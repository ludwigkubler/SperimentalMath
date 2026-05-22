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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i + max(range(i, m), key=lambda r: abs(A[r][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        return A

    def matrix_multiply(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0] * p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def construct_formal_group(instance):
        n = len(instance)
        G = [[0]*n for _ in range(n)]
        for clause in instance:
            for literal in clause:
                if literal > 0:
                    G[literal-1][(literal-1+n)%n] += 1
                else:
                    G[-literal-1][(literal-1+n)%n] -= 1
        return gaussian_elimination(G)

    def dpll_search_tree_height(instance):
        n = len(instance)
        stack = [(0, [])]
        max_height = 0
        while stack:
            node, assignment = stack.pop()
            if node == n:
                max_height = max(max_height, len(assignment))
                continue
            for literal in instance[node]:
                new_assignment = assignment[:]
                if literal > 0:
                    new_assignment.append(literal)
                else:
                    new_assignment.append(-literal)
                stack.append((node + 1, new_assignment))
        return max_height

    def minimal_rank(G):
        rank = 0
        for row in G:
            if any(row):
                rank += 1
        return rank

    n = random.randint(5, 40)
    instance = [[random.choice([-i, i]) for _ in range(n)] for _ in range(n)]
    
    formal_group = construct_formal_group(instance)
    minimal_rank_value = minimal_rank(formal_group)
    dpll_height = dpll_search_tree_height(instance)
    
    f_n = n**2  # Example polynomial function
    ratio = dpll_height / minimal_rank_value
    
    return {
        "metric_name": "Ratio of DPLL Search Tree Height to Minimal Rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= f_n,
        "counterexample": "" if ratio <= f_n else f"Instance with n={n} has minimal rank {minimal_rank_value} and DPLL height {dpll_height}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Instance with n={n} has minimal rank {minimal_rank_value} and DPLL height {dpll_height}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")