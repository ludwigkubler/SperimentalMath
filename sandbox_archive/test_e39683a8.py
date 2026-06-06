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
    
    def generate_cnf(n, m):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if not unit_clauses:
            p = random.choice([x for x in range(1, n+1)])
            if p in assignment:
                return dpll(clauses, assignment)
            else:
                return dpll(clauses, {**assignment, p: True}) or dpll(clauses, {**assignment, p: False})
        p = unit_clauses[0][0]
        if p < 0:
            p = -p
        new_assignment = {**assignment, p: True}
        new_clauses = [c for c in clauses if not any(x == p or x == -p for x in c)]
        if dpll(new_clauses, new_assignment):
            return True
        new_assignment = {**assignment, p: False}
        new_clauses = [c for c in clauses if not any(x == p or x == -p for x in c)]
        if dpll(new_clauses, new_assignment):
            return True
        return False

    def quiver_representation(clauses):
        n = len(clauses)
        Q = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if any(x == y or x == -y for x in clauses[i]) and any(x == y or x == -y for x in clauses[j]):
                    Q[i][j] = 1
                    Q[j][i] = 1
        return Q

    def min_order(Q):
        n = len(Q)
        visited = [False] * n
        order = 0
        
        def dfs(v):
            nonlocal order
            stack = [v]
            while stack:
                u = stack.pop()
                if not visited[u]:
                    visited[u] = True
                    for v in range(n):
                        if Q[u][v] == 1 and not visited[v]:
                            stack.append(v)
                            order += 1
        
        for i in range(n):
            if not visited[i]:
                dfs(i)
        
        return order

    n_max = 40
    instances_tested = 30
    total_order = 0
    total_path_length = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n, n * (n - 1) // 2)
        clauses = generate_cnf(n, m)
        Q = quiver_representation(clauses)
        order = min_order(Q)
        path_length = dpll(clauses, {})
        
        if path_length is None:
            continue
        
        total_order += math.log(order)
        total_path_length += path_length
    
    if instances_tested == 0:
        return {
            "metric_name": "log(min_order(Q(φ))) vs l(φ)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid CNF formulas generated"
        }
    
    mean_order = total_order / instances_tested
    mean_path_length = total_path_length / instances_tested
    correlation_coefficient = (instances_tested * total_order * total_path_length - sum(order * path_length for order, path_length in zip([math.log(order) for order in range(1, n_max+1)], [dpll(generate_cnf(n, m), {}) for n in range(5, n_max+1)]))) / (instances_tested * math.sqrt(sum((order - mean_order)**2 for order in range(1, n_max+1)) * sum((path_length - mean_path_length)**2 for path_length in [dpll(generate_cnf(n, m), {}) for n in range(5, n_max+1)])))
    
    return {
        "metric_name": "log(min_order(Q(φ))) vs l(φ)",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] is None or r["metric_value"] < 0.6 for r in results):
        print(f"RESULT: FALSIFIED counterexample=\"Correlation coefficient too low\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if r['conjecture_holds'] == False)]}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")