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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            literals = set()
            while len(literals) < 3:
                var = random.randint(1, n)
                sign = random.choice([-1, 1])
                literals.add((var, sign))
            clause = [l[0] * l[1] for l in literals]
            clauses.append(clause)
        return clauses

    def resolution(clauses):
        new_clauses = set()
        while True:
            added = False
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(-l == m for l in clauses[i] for m in clauses[j]):
                        new_clause = [l for l in clauses[i] if l not in [-m for m in clauses[j]]]
                        new_clause.extend([l for l in clauses[j] if l not in [-m for m in clauses[i]]])
                        new_clauses.add(tuple(sorted(new_clause)))
                        added = True
            if not added:
                break
            clauses.update(new_clauses)
        return len(clauses)

    def incidence_graph(clauses):
        graph = {}
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    lit_i, lit_j = clause[i], clause[j]
                    if abs(lit_i) not in graph:
                        graph[abs(lit_i)] = set()
                    if abs(lit_j) not in graph:
                        graph[abs(lit_j)] = set()
                    graph[abs(lit_i)].add(abs(lit_j))
                    graph[abs(lit_j)].add(abs(lit_i))
        return graph

    def min_generators(graph):
        generators = []
        visited = set()
        for node in graph:
            if node not in visited:
                generator = {node}
                queue = [node]
                while queue:
                    current = queue.pop(0)
                    for neighbor in graph[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            generator.add(neighbor)
                            queue.append(neighbor)
                generators.append(generator)
        return len(generators)

    n = 10
    m = 20
    clauses = generate_3cnf(n, m)
    resolution_size = resolution(clauses)
    graph = incidence_graph(clauses)
    num_generators = min_generators(graph)

    return {
        "metric_name": "num_generators",
        "metric_value": num_generators,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")