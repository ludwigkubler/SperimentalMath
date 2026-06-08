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
    
    def generate_d_regular_graph(n, d):
        if (n * d) % 2 != 0 or n < d + 1:
            return None
        graph = [[] for _ in range(n)]
        edges = set()
        for i in range(d):
            for j in range(i + 1, n):
                if len(graph[i]) >= d or len(graph[j]) >= d:
                    continue
                if (i, j) not in edges and (j, i) not in edges:
                    graph[i].append(j)
                    graph[j].append(i)
                    edges.add((i, j))
        return graph
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {v: 2 * v + 1 for v in range(n)}
        clauses = []
        for i in range(n):
            if len(graph[i]) < 2:
                continue
            clause = [literals[i]]
            for j in graph[i]:
                clause.append(-literals[j])
            clauses.append(clause)
            for u, v in itertools.combinations(graph[i], 2):
                new_literal = n * 2 + len(literals)
                literals[v] = new_literal
                clauses.append([new_literal, -literals[u]])
                clauses.append([new_literal, -literals[v]])
                clauses.append([-new_literal, literals[u], literals[v]])
        return literals, clauses
    
    def resolution_width(clauses):
        queue = [c for c in clauses if len(c) == 1]
        learned_clauses = []
        while queue:
            clause = queue.pop()
            literal = clause[0]
            for other_clause in clauses:
                if literal in other_clause:
                    new_clause = [l for l in other_clause if l != literal and -l not in other_clause]
                    if len(new_clause) == 1:
                        return abs(new_clause[0])
                    learned_clauses.append(new_clause)
        return float('inf')
    
    def alexander_orlik_solomon_complexity(graph):
        n = len(graph)
        if n < 2:
            return 0
        generators = []
        for i in range(n):
            if len(graph[i]) == 1:
                continue
            generator = [i]
            for j in graph[i]:
                if j not in generator:
                    generator.append(j)
            generators.append(generator)
        return len(generators)
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0
    support_count = 0
    
    for n in range(5, n_max + 1):
        for _ in range(n // d):  # Ensure at least 30 instances per seed
            graph = generate_d_regular_graph(n, d)
            if graph is None:
                continue
            literals, clauses = tseitin_formula(graph)
            width = resolution_width(clauses)
            complexity = alexander_orlik_solomon_complexity(graph)
            if width == float('inf'):
                continue
            instances_tested += 1
            total_metric_value += abs(complexity - width)
            if abs(complexity - width) <= 10 and abs(complexity / width - 1) <= 2/3:
                support_count += 1
    
    metric_name = "AOS(G) vs w(φ_G)"
    metric_value = total_metric_value / instances_tested
    conjecture_holds = support_count >= (instances_tested * 4 // 5)
    counterexample = "" if conjecture_holds else f"Instances tested: {instances_tested}, Support count: {support_count}"
    
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
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 80%\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE support_fraction < 80%")