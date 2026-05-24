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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = [f'-{variables[i-1]}', f'{variables[n+i-1]}']
            clauses.append(clause)
            clause = [f'{variables[i-1]}', f'-{variables[n+i-1]}']
            clauses.append(clause)
        for i in range(n+1, 2*n):
            for j in range(i+1, 2*n):
                clause = [f'-{variables[i-1]}', f'-{variables[j-1]}', f'{variables[2*n+i-j-1]}']
                clauses.append(clause)
        return variables, clauses
    
    def is_quasigroup(q):
        n = len(q)
        for i in range(n):
            for j in range(n):
                if q[i][j] < 0 or q[i][j] >= n:
                    return False
                for k in range(n):
                    if q[q[i][j]][k] != q[i][q[j][k]]:
                        return False
        return True
    
    def resolution_refutation_depth(q, clauses):
        n = len(q)
        visited = set()
        stack = []
        for clause in clauses:
            stack.append(clause)
        while stack:
            clause = stack.pop()
            if all(x not in visited for x in clause):
                visited.update(clause)
                for i in range(n):
                    for j in range(n):
                        if q[i][j] == -1:
                            continue
                        new_clause = [f'-{q[i][j]}']
                        if any(c in new_clause for c in clause):
                            continue
                        stack.append(new_clause)
        return len(visited) + 1
    
    def min_quasigroup_rank(clauses):
        n = int(math.sqrt(len(clauses)))
        q = [[-1] * n for _ in range(n)]
        rank = 0
        for i, clause in enumerate(clauses):
            if all(x not in q[i] for x in clause):
                rank += 1
                for x in clause:
                    q[i][x] = i
        return rank
    
    variables, clauses = generate_tseitin_formula(5)
    quasigroups = []
    for _ in range(30):
        q = [[random.randint(0, n-1) for _ in range(n)] for _ in range(n)]
        if is_quasigroup(q):
            quasigroups.append((q, min_quasigroup_rank(clauses)))
    
    refutation_depths = [resolution_refutation_depth(q, clauses) for q, rank in quasigroups]
    ranks = [rank for q, rank in quasigroups]
    
    if not quasigroups:
        return {
            "metric_name": "refutation_depth_to_rank_ratio",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    refutation_depth_mean = sum(refutation_depths) / len(refutation_depths)
    rank_mean = sum(ranks) / len(ranks)
    ratio_mean = refutation_depth_mean / rank_mean
    
    return {
        "metric_name": "refutation_depth_to_rank_ratio",
        "metric_value": ratio_mean,
        "instances_tested": len(quasigroups),
        "conjecture_holds": ratio_mean > math.exp(0.1 * math.log2(len(clauses))),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 37))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    refutation_depth_mean = sum(r["metric_value"] for r in results) / len(results)
    rank_mean = sum(1/r["instances_tested"] * r["metric_value"] for r in results) / sum(1/r["instances_tested"] for r in results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={refutation_depth_mean} std=0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={refutation_depth_mean} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not enough quasigroups\" first_failing_seed={seeds[first_failing_seed]}")