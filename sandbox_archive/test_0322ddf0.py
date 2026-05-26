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
    
    def generate_graph(n):
        if n <= 1:
            return []
        nodes = list(range(1, n+1))
        edges = set()
        for _ in range(int(n * (n - 1) / 4)):
            u, v = random.sample(nodes, 2)
            if u < v and (u, v) not in edges:
                edges.add((u, v))
        return nodes, edges
    
    def tseitin_formula(graph):
        n = len(graph[0])
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
        for u, v in graph[1]:
            clauses.append([-u, -v, u + v])
            clauses.append([-u, -v, -(u + v)])
            clauses.append([-u, v, u + v])
            clauses.append([-u, v, -(u + v)])
            clauses.append([u, -v, u + v])
            clauses.append([u, -v, -(u + v)])
        return clauses
    
    def resolution_length(clauses):
        stack = []
        while True:
            new_clauses = set()
            for clause in clauses:
                if not any(abs(lit) == abs(lit2) and lit != lit2 for lit in clause for lit2 in stack):
                    new_clauses.add(tuple(sorted(clause)))
            if len(new_clauses) == len(clauses):
                return len(stack)
            clauses = new_clauses
            for clause in clauses:
                if any(abs(lit) not in [abs(lit2) for lit2 in stack] and abs(lit) not in [abs(lit2) for lit2 in clause] for lit in clause):
                    stack.append(clause[0])
    
    def graphical_virtual_knot_rank(graph):
        n = len(graph[0])
        rank = 1
        for i in range(1, n+1):
            rank *= (i + 1)
        return rank
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    tseitin_clauses = tseitin_formula(graph)
    resolution_len = resolution_length(tseitin_clauses)
    knot_rank = graphical_virtual_knot_rank(graph)
    
    return {
        "metric_name": "rank",
        "metric_value": knot_rank,
        "instances_tested": 1,
        "conjecture_holds": abs(knot_rank - resolution_len) <= 2 * len(tseitin_clauses),
        "counterexample": "" if knot_rank == resolution_len else f"rank={knot_rank}, expected={resolution_len}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")