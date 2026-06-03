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
        if (n * d) % 2 != 0 or d > n - 1:
            return None
        graph = {i: [] for i in range(n)}
        edges = set()
        while len(edges) < (n * d) // 2:
            u, v = random.sample(range(n), 2)
            if u == v or (u, v) in edges or (v, u) in edges:
                continue
            graph[u].append(v)
            graph[v].append(u)
            edges.add((u, v))
        return graph

    def calculate_mli(graph):
        n = len(graph)
        mli = 0
        for i in range(n):
            for j in range(i + 1, n):
                if j not in graph[i]:
                    mli += 1
        return mli

    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        queue = cnf[:]
        resolvents = set()
        while queue:
            clause = queue.pop(0)
            for other_clause in queue:
                if any(abs(lit) == abs(other_lit) for lit, other_lit in zip(clause, other_clause)):
                    new_clause = [lit for lit in clause + other_clause if abs(lit) != abs(other_lit)]
                    new_clause.sort()
                    resolvent = tuple(new_clause)
                    if resolvent not in resolvents:
                        resolvents.add(resolvent)
                        queue.append(list(resolvent))
        return len(resolvents)

    def generate_cnf(n):
        cnf = []
        for i in range(1, n + 1):
            clause = [-i, -(-i % (n // 2) + 1)]
            cnf.append(clause)
        return cnf

    n = random.randint(5, 40)
    d = random.randint(2, min(n - 1, 3))
    graph = generate_d_regular_graph(n, d)
    if not graph:
        return {
            "metric_name": "mli(G)",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mli = calculate_mli(graph)
    cnf = generate_cnf(n)
    width = resolution_width(cnf)

    return {
        "metric_name": "mli(G)",
        "metric_value": mli,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mli <= width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mli(G) > width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")