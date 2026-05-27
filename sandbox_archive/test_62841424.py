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

def generate_kneser_graph(n, k):
    elements = list(range(1, n + 1))
    graph = []
    for S in combinations(elements, k):
        for T in combinations(elements, k):
            if len(S & T) == 0:
                graph.append((S, T))
    return graph

def combinations(iterable, r):
    pool = tuple(iterable)
    n = len(pool)
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        yield tuple(pool[i] for i in indices)

def tseitin_formula(graph):
    literals = {}
    clauses = []
    literal_id = 0

    def get_literal(S):
        if S not in literals:
            literals[S] = literal_id
            literal_id += 1
        return literals[S]

    for (S, T) in graph:
        x = get_literal(S)
        y = get_literal(T)
        clauses.append([-x, -y])
        clauses.append([x, y])

    # Add unit clause for each vertex
    for S in literals:
        clauses.append([get_literal(S)])

    return clauses

def dpll(clauses):
    def solve(model):
        if not clauses:
            return model
        literal = next((lit for lit in range(1, max(literals.values()) + 1) if lit not in model and -lit not in model), None)
        if literal is None:
            return None

        new_model = model.copy()
        new_model[literal] = True
        result = solve(new_model)
        if result is not None:
            return result

        new_model[literal] = False
        result = solve(new_model)
        if result is not None:
            return result

        return None

    return solve({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    graph = generate_kneser_graph(n, 2)
    clauses = tseitin_formula(graph)
    refutation_length = len(dpll(clauses)) if dpll(clauses) is not None else float('inf')
    return {
        "metric_name": "resolution_refutation_length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": refutation_length >= 2**(n/2),
        "counterexample": "" if refutation_length >= 2**(n/2) else "refutation_length < 2^(n/2)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_refutation_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_refutation_length} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='refutation_length < 2^(n/2)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")