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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(len(clause)) for j in range(i+1, len(clause))):
                clauses.append(clause)
        return clauses
    
    def incidence_matrix(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        M = [[0] * (n + 1) for _ in range(len(cnf))]
        for i, clause in enumerate(cnf):
            for lit in clause:
                M[i][abs(lit)] += 1
        return M
    
    def trace(M):
        n = len(M)
        return sum(M[i][i] for i in range(n))
    
    def gaussian_elimination(A):
        n = len(A)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                if j != i:
                    factor = -A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] += factor * A[i][k]
        rank = sum(1 for row in A if any(row))
        return rank
    
    def clause_tree_width(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        graph = [[] for _ in range(n + 1)]
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    graph[abs(clause[i])].append(abs(clause[j]))
                    graph[abs(clause[j])].append(abs(clause[i]))
        
        def dfs(node, parent):
            if node == n:
                return 0
            max_width = 0
            for neighbor in graph[node]:
                if neighbor != parent:
                    width = dfs(neighbor, node)
                    max_width = max(max_width, width)
            return max_width + 1
        
        return dfs(1, -1) - 1
    
    def quadratic_form_rank(cnf):
        M = incidence_matrix(cnf)
        return gaussian_elimination(M)
    
    n_max = 0
    metric_values = []
    instances_tested = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            cnf = generate_cnf(n)
            r_q = quadratic_form_rank(cnf)
            w_c = clause_tree_width(cnf)
            metric_values.append((r_q, w_c))
            instances_tested += 1
    
    if not metric_values:
        return {
            "metric_name": "quadratic_form_rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_valid_cnf_generated"
        }
    
    r_q_values, w_c_values = zip(*metric_values)
    mean_r_q = sum(r_q_values) / len(r_q_values)
    mean_w_c = sum(w_c_values) / len(w_c_values)
    correlation_coefficient = sum((r_q - mean_r_q) * (w_c - mean_w_c) for r_q, w_c in metric_values) / (len(metric_values) * math.sqrt(sum((r_q - mean_r_q)**2 for r_q in r_q_values)) * math.sqrt(sum((w_c - mean_w_c)**2 for w_c in w_c_values)))
    
    return {
        "metric_name": "quadratic_form_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")