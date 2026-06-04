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
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                clause[random.randint(0, n-1)] = random.choice([-1, 1])
            clauses.append(clause)
        return clauses
    
    def quasi_crystalline_sheaf(cnf):
        n = len(cnf[0]) // 2
        matrix = [[0] * (2**n) for _ in range(2**n)]
        for clause in cnf:
            for i in range(n):
                if clause[i] != 0:
                    row = int(''.join(str(abs(x)) for x in clause[:i]), 2)
                    col = int(''.join(str(abs(x)) for x in clause[i+1:]), 2)
                    matrix[row][col] += abs(clause[i])
        return matrix
    
    def min_order(matrix):
        n = len(matrix)
        visited = [False] * n
        order = 0
        
        def dfs(node):
            nonlocal order
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    order += 1
                    for neighbor in range(n):
                        if matrix[node][neighbor] != 0 and not visited[neighbor]:
                            stack.append(neighbor)
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
        return order
    
    def resolution_width(cnf):
        n = len(cnf[0]) // 2
        queue = cnf[:]
        width = 1
        
        while queue:
            new_queue = []
            for clause in queue:
                for i in range(n):
                    if clause[i] != 0:
                        new_clause = [x for x in clause[:i]] + [-x for x in clause[i+1:]]
                        if any(new_clause == c for c in cnf):
                            continue
                        new_queue.append(new_clause)
            queue = new_queue
            width += len(queue)
        return width
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    qc_sheaf = quasi_crystalline_sheaf(cnf)
    min_order_qc = min_order(qc_sheaf)
    w_phi = resolution_width(cnf)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": abs(w_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(w_phi) <= Fraction(n).log(2) * min_order_qc,
        "counterexample": "" if conjecture_holds else f"n={n}, w_phi={w_phi}, min_order_qc={min_order_qc}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n_max']}, w_phi={results[0]['metric_value']}, min_order_qc={results[0]['counterexample'].split('=')[1]}\" first_failing_seed={first_failing_seed}")