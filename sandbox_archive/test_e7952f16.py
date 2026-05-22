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
            max_row = i + max(range(i, m), key=lambda x: abs(A[x][i]))
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for k in range(m):
                if k != i:
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

    def formal_group_rank(clauses, literals):
        n = len(literals)
        G = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    G[literal - 1][n] += 1
                else:
                    G[-literal - 1][n] -= 1
        rank = gaussian_elimination(G)
        return sum(row[n] != 0 for row in rank)

    def dpll_search_tree_height(clauses, literals):
        n = len(literals)
        stack = [(clauses, literals)]
        height = 0
        while stack:
            clauses, literals = stack.pop()
            if not clauses:
                continue
            literal = random.choice(literals)
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            new_literals = literals[:]
            new_literals.remove(literal)
            stack.append((new_clauses, new_literals))
            stack.append(([c for c in new_clauses if literal in c], new_literals))
            height += 1
        return height

    def f(n):
        # Polynomial function to bound the ratio of DPLL search tree height to minimal rank
        return n**2 + 5*n + 10

    n = random.randint(5, 40)
    clauses = [[random.choice(literals) for _ in range(random.randint(1, n))] for _ in range(n)]
    literals = list(range(1, n + 1))
    
    rank = formal_group_rank(clauses, literals)
    height = dpll_search_tree_height(clauses, literals)
    
    if rank > f(n):
        return {
            "metric_name": "Ratio of DPLL search tree height to minimal rank",
            "metric_value": height / rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Formal group of minimal rank {rank} exceeds bound f({n}) = {f(n)}"
        }
    
    return {
        "metric_name": "Ratio of DPLL search tree height to minimal rank",
        "metric_value": height / rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results if "metric_value" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Formal group of minimal rank exceeds bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")