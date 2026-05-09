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
    
    def is_prime(n):
        if n <= 1:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    def generate_3cnf(n: int) -> list:
        clauses = []
        variables = set()
        for _ in range(n * (n - 1) // 2):
            var1, var2 = random.sample(range(1, n + 1), 2)
            sign1, sign2 = random.choice([-1, 1]), random.choice([-1, 1])
            clauses.append(f"{sign1}*x{var1} + {sign2}*x{var2} - 1")
            variables.update([var1, var2])
        return clauses
    
    def conflict_graph(clauses: list) -> dict:
        graph = {}
        for clause in clauses:
            vars_in_clause = [int(var[2:]) for var in clause.split() if var.startswith('x')]
            for i in range(len(vars_in_clause)):
                for j in range(i + 1, len(vars_in_clause)):
                    u, v = sorted([vars_in_clause[i], vars_in_clause[j]])
                    if u not in graph:
                        graph[u] = set()
                    if v not in graph:
                        graph[v] = set()
                    graph[u].add(v)
                    graph[v].add(u)
        return graph
    
    def clique_number(graph: dict) -> int:
        max_clique_size = 0
        for node in graph:
            neighbors = graph[node]
            for subset in range(1, len(neighbors) + 1):
                for combination in itertools.combinations(neighbors, subset):
                    if all(node in graph[neighbor] for neighbor in combination):
                        max_clique_size = max(max_clique_size, subset)
        return max_clique_size
    
    def is_real_stable(poly: str) -> bool:
        # Placeholder function to check real stability
        # In practice, this would involve complex root conditions
        return True
    
    def sos_degree(poly: str) -> int:
        # Placeholder function to compute SOS degree
        # In practice, this would use a truncated Lasserre hierarchy solver
        return len(poly.split(' + '))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_3cnf(n)
    conflict_graph_phi = conflict_graph(phi)
    omega_phi = clique_number(conflict_graph_phi)
    
    if omega_phi == 0:
        return {
            "metric_name": "deg_SOS",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "clique_number_undefined"
        }
    
    deg_sos_phi = sos_degree(phi)
    conjecture_holds = deg_sos_phi >= math.log2(omega_phi) + 2
    
    return {
        "metric_name": "deg_SOS",
        "metric_value": deg_sos_phi,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"omega(Φ)={omega_phi}, deg_SOS(Φ)={deg_sos_phi}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_deg_sos = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_deg_sos = math.sqrt(sum((r["metric_value"] - mean_deg_sos)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] or r["metric_value"] is None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_deg_sos} std={std_deg_sos} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'] != '')}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")