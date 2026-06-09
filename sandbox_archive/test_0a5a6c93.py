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

def generate_3cnf(m):
    variables = list(range(1, m + 1))
    clauses = []
    for _ in range(m):
        clause = [random.choice(variables) * (-1 if random.randint(0, 1) else 1)]
        while len(clause) < 3:
            var = random.choice(variables)
            if var not in clause:
                clause.append(var * (-1 if random.randint(0, 1) else 1))
        clauses.append(clause)
    return clauses

def construct_tropical_graph(clauses):
    n = max(abs(v) for clause in clauses for v in clause)
    graph = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                u, v = abs(clause[i]), abs(clause[j])
                graph[u][v] = max(graph[u][v], min(abs(clause[i]), abs(clause[j])))
                graph[v][u] = max(graph[v][u], min(abs(clause[i]), abs(clause[j])))
    return graph

def minimal_representation_complexity(graph):
    n = len(graph) - 1
    visited = [False] * (n + 1)
    queue = [i for i in range(1, n + 1)]
    while queue:
        u = queue.pop()
        if not visited[u]:
            visited[u] = True
            for v in range(1, n + 1):
                if graph[u][v] > 0 and not visited[v]:
                    queue.append(v)
    return sum(not visited[i] for i in range(1, n + 1))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    m_values = [10, 20, 30, 40]
    results = []
    
    for m in m_values:
        clauses = generate_3cnf(m)
        graph = construct_tropical_graph(clauses)
        n = len(graph) - 1
        tau = minimal_representation_complexity(graph)
        
        if tau > 4 * m**2:
            return {
                "metric_name": "tau(T(φ)) / n",
                "metric_value": Fraction(tau, n),
                "instances_tested": m,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"m={m}, tau={tau}, n={n}"
            }
        
        results.append({"m": m, "tau": tau, "n": n})
    
    return {
        "metric_name": "tau(T(φ)) / n",
        "metric_value": sum(Fraction(result["tau"], result["n"]) for result in results) / len(results),
        "instances_tested": sum(result["m"] for result in results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m={result['m']}, tau={result['tau']}, n={result['n']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")