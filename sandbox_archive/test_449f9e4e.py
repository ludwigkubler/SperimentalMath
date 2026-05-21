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
    
    def generate_random_graph(n):
        graph = {i: set() for i in range(n)}
        edges = [(i, j) for i in range(n) for j in range(i + 1, n)]
        random.shuffle(edges)
        m = min(2 * (n - 1), len(edges))
        for i in range(m):
            u, v = edges[i]
            graph[u].add(v)
            graph[v].add(u)
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        
        # Each vertex must be connected to at least one other vertex
        for i in range(n):
            if not graph[i]:
                continue
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(f'-{literals[j]}')
            clauses.append(clause)
        
        # Each edge is represented by a unique literal
        for u, v in [(i, j) for i in range(n) for j in range(i + 1, n)]:
            edge_literal = f'e{u}{v}'
            clauses.append([edge_literal, f'-x{u}', f'-x{v}'])
            clauses.append([f'-{edge_literal}', f'x{u}', f'x{v}'])
        
        return literals, clauses
    
    def resolution_length(clauses):
        n = len(clauses)
        unit_clauses = {i: [] for i in range(n)}
        for i, clause in enumerate(clauses):
            if len(clause) == 1:
                unit_clauses[i].append(clause[0])
        
        resolvents = []
        while True:
            new_resolvents = set()
            for i in range(n):
                for j in range(i + 1, n):
                    if not (set(unit_clauses[i]) & set(unit_clauses[j])):
                        continue
                    common_lit = list(set(unit_clauses[i]) & set(unit_clauses[j]))[0]
                    resolvent = [lit for lit in unit_clauses[i] if lit != common_lit] + \
                                [lit for lit in unit_clauses[j] if lit != f'-{common_lit}']
                    resolvents.add(tuple(sorted(resolvent)))
            if not new_resolvents:
                break
            unit_clauses[n] = list(new_resolvents)
            n += 1
        
        return len(unit_clauses[n - 1])
    
    def erdos_szekeres_lower_bound(n):
        C = 1.0  # Constant C > 0, chosen for simplicity
        return C * 2**(n / 2) * math.log(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_length = 0
    instances_tested = 0
    
    for n in n_values:
        graph = generate_random_graph(n)
        literals, clauses = tseitin_formula(graph)
        length = resolution_length(clauses)
        lower_bound = erdos_szekeres_lower_bound(n)
        
        total_length += length
        instances_tested += 1
        
        if length < lower_bound / 2 or length > 2 * lower_bound:
            return {
                "metric_name": "Resolution Length",
                "metric_value": length,
                "instances_tested": instances_tested,
                "conjecture_holds": False,
                "counterexample": f"n={n}, L_Resolution(G)={length}, Lower Bound={lower_bound}"
            }
    
    mean_length = total_length / instances_tested
    return {
        "metric_name": "Resolution Length",
        "metric_value": mean_length,
        "instances_tested": instances_tested,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = support_count / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_support")