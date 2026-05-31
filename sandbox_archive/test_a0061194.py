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
            for j in range(n):
                if j != i:
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def min_rank(A):
        rank = 0
        A = gaussian_elimination(A)
        for row in A:
            if any(row):
                rank += 1
        return rank

    def tseitin_formula(n, edges):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for u, v in edges:
            clauses.append([f'-{u}', f'{v}'])
            clauses.append([f'-{v}', f'{u}'])
            clauses.append([f'-{u}', f'-{v}', f'x{random.randint(1, n)}'])
        return variables, clauses

    def resolution_width(clauses):
        stack = []
        visited = set()
        for clause in clauses:
            if len(clause) == 1:
                stack.append(clause[0])
            else:
                visited.add(tuple(sorted(clause)))
        while stack:
            literal = stack.pop()
            if literal.startswith('-'):
                literal = literal[1:]
                for clause in clauses:
                    if literal in clause:
                        new_clause = [l for l in clause if l != literal and not l.startswith(f'-{literal}')]
                        if len(new_clause) == 1:
                            stack.append(new_clause[0])
                        else:
                            visited.add(tuple(sorted(new_clause)))
        return len(visited)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        edges = [(random.randint(1, n), random.randint(1, n)) for _ in range(n * (n - 1) // 2)]
        variables, clauses = tseitin_formula(n, edges)
        M = [[0] * n for _ in range(n)]
        for u, v in edges:
            M[u-1][v-1] = 1
            M[v-1][u-1] = 1
        
        rank = min_rank(M)
        width = resolution_width(clauses)
        
        results.append({
            "n": n,
            "rank": rank,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "min_rank_over_width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratios = [r["rank"] / r["width"] for r in results if r["width"] > 0]
    if not ratios:
        return {
            "metric_name": "min_rank_over_width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "resolution_width_zero"
        }
    
    mean_ratio = sum(ratios) / len(ratios)
    support_fraction = sum(0.5 <= ratio <= 1.5 for ratio in ratios) / len(ratios)
    
    return {
        "metric_name": "min_rank_over_width",
        "metric_value": mean_ratio,
        "instances_tested": len(ratios),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": support_fraction >= 0.9,
        "counterexample": "" if support_fraction >= 0.9 else f"mean_ratio={mean_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")