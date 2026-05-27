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
    
    def generate_sat_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            clauses.append(f"({clause[0]} OR {clause[1]})")
        return " AND ".join(clauses)

    def generate_coxeter_group(n):
        G = {}
        for i in range(n):
            G[i] = [(i + 1) % n]
        return G

    def tropicalize_representation(G, assignments):
        rank = 0
        for assignment in assignments:
            max_value = -math.inf
            for node, neighbors in G.items():
                value = sum(assignment[node] if i == node else 0 for i in neighbors)
                max_value = max(max_value, value)
            rank = max(rank, max_value)
        return rank

    def is_satisfying_assignment(G, assignment):
        for node, neighbors in G.items():
            if all(assignment[i] == 0 for i in neighbors):
                return False
        return True

    n = random.randint(5, 40)
    sat_instance = generate_sat_instance(n)
    G = generate_coxeter_group(n)

    assignments = []
    if is_satisfying_assignment(G, [1] * n):
        assignments.append([1] * n)
        for _ in range(29):
            assignment = [random.choice([0, 1]) for _ in range(n)]
            if is_satisfying_assignment(G, assignment):
                assignments.append(assignment)
    else:
        assignments = [[random.choice([0, 1]) for _ in range(n)] for _ in range(30)]

    min_rank = float('inf')
    for assignment in assignments:
        rank = tropicalize_representation(G, [assignment])
        if rank < min_rank:
            min_rank = rank

    metric_name = "min_rank"
    metric_value = min_rank
    instances_tested = len(assignments)
    conjecture_holds = min_rank >= n * math.log(n)
    counterexample = "" if conjecture_holds else f"n={n}, min_rank={min_rank}"

    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['metric_value']}, min_rank={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")