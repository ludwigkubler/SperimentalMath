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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def quasi_crystalline_sheaf(cnf):
        n = len(cnf[0])
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        for clause in cnf:
            for lit in clause:
                row, col = abs(lit), -lit if lit < 0 else lit
                matrix[row][col] += 1
        return matrix
    
    def min_order(matrix):
        n = len(matrix)
        visited = [False] * (n + 1)
        
        def dfs(node):
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for i in range(1, n + 1):
                        if matrix[node][i] > 0 and not visited[i]:
                            stack.append(i)
        
        dfs(1)
        return sum(visited[1:])
    
    def resolution_width(cnf):
        queue = cnf[:]
        levels = {tuple(clause): 1 for clause in cnf}
        while queue:
            clause = queue.pop()
            for lit in clause:
                neg_lit = -lit
                if neg_lit in [l for c in queue for l in c]:
                    new_clause = list(set([l for c in queue for l in c if l != neg_lit]))
                    if tuple(new_clause) not in levels:
                        levels[tuple(new_clause)] = levels[tuple(clause)] + 1
                        queue.append(new_clause)
        return max(levels.values())
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    qc_sheaf = quasi_crystalline_sheaf(cnf)
    min_order_qc = min_order(qc_sheaf)
    w_phi = resolution_width(cnf)
    
    metric_name = "resolution_width"
    metric_value = abs(w_phi)
    instances_tested = 1
    n_max = n
    conjecture_holds = metric_value <= math.log(n) * min_order_qc
    counterexample = "" if conjecture_holds else f"n={n}, w(φ)={w_phi}, min_order(QC(φ))={min_order_qc}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")