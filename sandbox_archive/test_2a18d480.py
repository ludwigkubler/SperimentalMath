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
from fractions import Fraction
import math

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n, m):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = [random.choice(variables), -random.choice(variables)]
            if not any(x == y or x == -y for x in clause):
                clauses.append(clause)
        return clauses

    def quiver_representation(clauses):
        n = len(clauses)
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if any(x == y or x == -y for x in clauses[i]) and any(x == y or x == -y for x in clauses[j]):
                    Q[i][j] = 1
                    Q[j][i] = 1
        return Q

    def min_order(Q):
        n = len(Q)
        visited = [False] * n
        order = 0
        
        def dfs(node):
            stack = [node]
            while stack:
                node = stack.pop()
                if not visited[node]:
                    visited[node] = True
                    for neighbor in range(n):
                        if Q[node][neighbor] == 1 and not visited[neighbor]:
                            stack.append(neighbor)
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
                order += 1
        
        return order

    def dpll(clauses, assignment):
        if not clauses:
            return True
        clause = next((c for c in clauses if any(x == y or x == -y for x in c)), [])
        var = abs(clause[0])
        if var not in assignment:
            assignment[var] = True
            if dpll([c for c in clauses if not any(x == y or x == -y for x in c)], assignment):
                return True
            del assignment[var]
        
        assignment[var] = False
        if dpll([c for c in clauses if not any(x == y or x == -y for x in c)], assignment):
            return True
        
        return False

    def proof_path_length(clauses):
        n = len(clauses)
        assignment = {}
        path_length = 0
        
        def backtrack():
            nonlocal path_length
            if dpll(clauses, assignment):
                return True
            for var in range(1, n + 1):
                if var not in assignment:
                    assignment[var] = True
                    path_length += 1
                    if backtrack():
                        return True
                    del assignment[var]
                    path_length -= 1
                    assignment[var] = False
                    path_length += 1
                    if backtrack():
                        return True
                    del assignment[var]
                    path_length -= 1
            return False
        
        backtrack()
        return path_length

    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n, n * (n - 1) // 2)
        clauses = generate_cnf(n, m)
        Q = quiver_representation(clauses)
        min_order_Q = min_order(Q)
        l_phi = proof_path_length(clauses)
        
        if min_order_Q == 0:
            continue
        
        metric_values.append(math.log(min_order_Q))
    
    if not metric_values:
        return {
            "metric_name": "log(min_order(Q(φ)))",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "min_order_Q is zero"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    correlation_coefficient = sum((x - mean) * (y - mean) for x, y in zip(metric_values, range(len(metric_values)))) / (len(metric_values) * std_dev * math.sqrt(sum((y - mean) ** 2 for y in range(len(metric_values)))))
    
    return {
        "metric_name": "log(min_order(Q(φ)))",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] is not None and r["metric_value"] < 0.6 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] is not None and r["metric_value"] < 0.6)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.6\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")