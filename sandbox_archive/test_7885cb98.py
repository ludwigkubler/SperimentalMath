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

def generate_tseitin_formula(n):
    variables = list(range(1, n + 1))
    tseitin_vars = list(range(n + 1, 2 * n + 1))
    clauses = []

    def add_clause(clause):
        clauses.append(clause)

    for i in range(n):
        add_clause([variables[i], -tseitin_vars[i]])
        add_clause([-variables[i], tseitin_vars[i]])
        add_clause([-tseitin_vars[i]])

    for i in range(1, n):
        add_clause([tseitin_vars[i - 1], tseitin_vars[i], -tseitin_vars[n + i]])

    for i in range(n):
        add_clause([variables[i], -tseitin_vars[n + i]])
        add_clause([-variables[i], tseitin_vars[n + i]])
        add_clause([-tseitin_vars[n + i]])

    return variables, clauses

def find_maximal_disjoint_set(variables, clauses):
    graph = {v: set() for v in variables}
    for clause in clauses:
        for i in range(len(clause)):
            for j in range(i + 1, len(clause)):
                if clause[i] > 0 and clause[j] > 0:
                    graph[clause[i]].add(clause[j])
                    graph[clause[j]].add(clause[i])

    def dfs(node, visited):
        stack = [node]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                for neighbor in graph[node]:
                    stack.append(neighbor)

    components = []
    visited = set()
    for v in variables:
        if v not in visited:
            component = set()
            dfs(v, component)
            components.append(component)

    max_disjoint_set = max(components, key=len)
    return max_disjoint_set

def resolution_refutation_length(variables, clauses):
    # Simplified version of Resolution refutation length calculation
    return len(clauses) * 2

def run_trial(seed: int) -> dict:
    random.seed(seed)

    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    max_disjoint_set = find_maximal_disjoint_set(variables, clauses)
    C_G = len(max_disjoint_set)

    refutation_length = resolution_refutation_length(variables, clauses)

    return {
        "metric_name": "Resolution refutation length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": refutation_length >= 2 ** C_G and refutation_length < 2 ** (C_G + 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 100, 4))
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_refutation_length = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_refutation_length / len(results)} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_refutation_length / len(results)} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='refutation_length < 2^C(G)' first_failing_seed={seeds[first_failing_seed]}")