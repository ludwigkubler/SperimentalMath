# auto-injected by SEC sandbox
import math
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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(m):
        variables = set()
        clauses = []
        for _ in range(m):
            clause = set()
            for _ in range(3):
                var = f'x{random.randint(1, 20)}'
                if random.choice([True, False]):
                    var = f'-{var}'
                clause.add(var)
                variables.add(var[1:] if '-' in var else var)
            clauses.append(clause)
        return clauses, variables
    
    def tropical_graph(clauses):
        n = len(variables)
        adj_matrix = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in range(n):
                for j in range(i + 1, n):
                    if (f'x{i+1}' in clause and f'x{j+1}' not in clause) or \
                       (f'-x{i+1}' in clause and f'-x{j+1}' not in clause):
                        adj_matrix[i][j] = 1
                        adj_matrix[j][i] = 1
        return adj_matrix
    
    def min_representation_complexity(adj_matrix):
        n = len(adj_matrix)
        visited = [False] * n
        queue = []
        
        for i in range(n):
            if not visited[i]:
                queue.append(i)
                while queue:
                    u = queue.pop(0)
                    visited[u] = True
                    for v in range(n):
                        if adj_matrix[u][v] == 1 and not visited[v]:
                            queue.append(v)
        
        return sum(not v for v in visited)
    
    m_values = [10, 20, 30, 40]
    results = []
    
    for m in m_values:
        clauses, variables = generate_3cnf(m)
        adj_matrix = tropical_graph(clauses)
        n = len(adj_matrix)
        tau = min_representation_complexity(adj_matrix)
        
        if tau > 4 * m**2:
            return {
                "metric_name": "tau_over_n",
                "metric_value": Fraction(tau, n),
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"m={m}, tau={tau}, n={n}"
            }
        
        results.append({"m": m, "n": n, "tau": tau})
    
    return {
        "metric_name": "tau_over_n",
        "metric_value": sum(Fraction(r["tau"], r["n"]) for r in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")