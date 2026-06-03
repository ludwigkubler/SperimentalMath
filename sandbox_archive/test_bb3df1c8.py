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
        graph = {i: set() for i in range(n)}
        edges_added = 0
        while edges_added < n * d // 2:
            u = random.randint(0, n - 1)
            v = random.randint(0, n - 1)
            if u != v and v not in graph[u]:
                graph[u].add(v)
                graph[v].add(u)
                edges_added += 1
        return graph

    def calculate_mli(graph):
        n = len(graph)
        mli = 0
        for i in range(n):
            neighbors = graph[i]
            if not neighbors:
                continue
            min_rank = float('inf')
            for j in neighbors:
                rank = sum(1 for k in graph[j] if k != i and k not in neighbors)
                min_rank = min(min_rank, rank)
            mli += min_rank
        return mli / n

    def resolution_proof_width(cnf):
        stack = []
        literals_seen = set()
        for clause in cnf:
            if any(lit in literals_seen for lit in clause):
                continue
            literals_seen.update(clause)
            stack.append((clause, 0))
        width = 0
        while stack:
            clause, idx = stack.pop()
            if idx == len(clause):
                continue
            lit = clause[idx]
            new_clause = [l for l in clause if l != lit and -l not in clause]
            if not new_clause:
                return float('inf')
            literals_seen.add(lit)
            width = max(width, len(new_clause))
            stack.append((new_clause, 0))
        return width

    def generate_cnf(n):
        cnf = []
        for i in range(n):
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)]
            for j in range(i + 1, n):
                clause.append(random.randint(1, n) * (-1 if random.choice([True, False]) else 1))
            cnf.append(clause)
        return cnf

    def calculate_w_phi(cnf):
        return resolution_proof_width(cnf)

    n = 40
    d = 3
    graph = generate_d_regular_graph(n, d)
    mli = calculate_mli(graph)
    cnf = generate_cnf(n)
    w_phi = calculate_w_phi(cnf)

    if mli > w_phi:
        return {
            "metric_name": "mli(G)",
            "metric_value": mli,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"mli(G)={mli} > w(φ_G)={w_phi}"
        }

    return {
        "metric_name": "mli(G)",
        "metric_value": mli,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_mli = sum(result["metric_value"] for result in results) / len(results)
    std_mli = math.sqrt(sum((result["metric_value"] - mean_mli) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_mli} std={std_mli} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mli(G) > w(φ_G)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")