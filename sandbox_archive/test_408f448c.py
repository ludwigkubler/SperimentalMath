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
    
    def generate_d_regular_graph(d, n):
        if d * (n - 1) % 2 != 0:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(1, n):
            for j in range(i + 1, n):
                if random.randint(0, 1) == 0 and (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [literals[i]]
            for neighbor in graph[i]:
                clause.append(f'-{literals[neighbor]}')
            clauses.append(clause)
        for i in range(n):
            for j in range(i + 1, n):
                clauses.append([f'-{literals[i]}', f'-{literals[j]}'])
                clauses.append([f'{literals[i]}', f'{literals[j]}'])
        return literals, clauses
    
    def dpll(clauses, model={}):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if not unit_clauses:
            return False
        literal = unit_clauses[0][0]
        polarity = literal[0] != '-'
        literal = literal[1:] if polarity else literal
        new_model = model.copy()
        new_model[literal] = polarity
        new_clauses = []
        for clause in clauses:
            if literal not in clause and '-' + literal not in clause:
                new_clauses.append(clause)
            elif literal in clause:
                continue
            else:
                new_clause = [l for l in clause if l != '-' + literal]
                new_clauses.append(new_clause)
        return dpll(new_clauses, new_model) or dpll(new_clauses, model.copy())
    
    def mls(graph):
        n = len(graph)
        rank = 0
        for i in range(n):
            neighbors = graph[i]
            if not neighbors:
                continue
            subgraph = [j for j in range(n) if j != i and j not in neighbors]
            subgraph_rank = mls(subgraph)
            if subgraph_rank is None:
                return None
            rank += 1 + subgraph_rank
        return rank
    
    def psat(clauses):
        literals, clauses = tseitin_formula(graph)
        model = {}
        for literal, polarity in zip(literals, [False] * len(literals)):
            model[literal] = polarity
        return dpll(clauses, model)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        graph = generate_d_regular_graph(random.randint(3, 10), n)
        if graph is None:
            continue
        instances_tested += 1
        mls_value = mls(graph)
        if mls_value is None:
            continue
        psat_value = psat(graph)
        if psat_value is None:
            continue
        metric_value = mls_value / psat_value
        total_metric_value += metric_value
        
        if metric_value < 0.75 * psat_value:
            conjecture_holds = False
            counterexample = f"Graph with n={n}, mls(G)={mls_value}, PSAT(φ_G')={psat_value}"
    
    return {
        "metric_name": "mls(G) / PSAT(φ_G')",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[sum(1 for r in results if not r['conjecture_holds'])].get('counterexample', 'unknown')}\") first_failing_seed={seeds[sum(1 for r in results if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support for conjecture")