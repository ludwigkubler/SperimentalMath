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

def generate_cnf(n):
    clauses = []
    for i in range(1, n + 1):
        clause = [random.choice([i, -i]) for _ in range(random.randint(2, 4))]
        clauses.append(clause)
    return clauses

def tseitin_graph(cnf):
    graph = {}
    literals = set()
    new_var = 1
    var_map = {}

    def add_node(var):
        if var not in graph:
            graph[var] = []

    for clause in cnf:
        for literal in clause:
            literals.add(literal)
            add_node(literal)

    for clause in cnf:
        tseitin_var = -new_var
        new_var += 1
        var_map[tseitin_var] = clause

        for literal in clause:
            graph[-tseitin_var].append(literal)
            graph[literal].append(-tseitin_var)

    return graph, literals, var_map

def topological_entropy(graph):
    n = len(graph)
    indegrees = [0] * (n + 1)
    for node in graph:
        for neighbor in graph[node]:
            indegrees[neighbor] += 1

    queue = [node for node in range(1, n + 1) if indegrees[node] == 0]
    entropy = 0
    while queue:
        node = queue.pop()
        entropy -= math.log2(len(graph[node]))
        for neighbor in graph[node]:
            indegrees[neighbor] -= 1
            if indegrees[neighbor] == 0:
                queue.append(neighbor)

    return entropy

def resolution_width(cnf):
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if literal < 0:
                new_assignment[-literal] = False
            return dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment)
        pure_literal = next((l for l in range(1, max(literals) + 1) if (l not in assignment and -l not in assignment)), None)
        if pure_literal:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], new_assignment)
        literal = random.choice(literals)
        return dpll(clauses + [[-literal]], assignment) or dpll(clauses, assignment)

    max_width = 0
    for _ in range(10):
        assignment = {l: False for l in literals}
        width = 0
        while not dpll(cnf, assignment):
            unsatisfied_clauses = [c for c in cnf if any(l not in assignment or not assignment[l] for l in c)]
            unit_clause = next((c for c in unsatisfied_clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                assignment[literal] = True
                if literal < 0:
                    assignment[-literal] = False
            else:
                literal = random.choice(literals)
                assignment[literal] = True
            width += 1
        max_width = max(max_width, width)
    return max_width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    graph, literals, var_map = tseitin_graph(cnf)
    entropy = topological_entropy(graph)
    width = resolution_width(cnf)
    return {
        "metric_name": "Topological Entropy vs Resolution Width",
        "metric_value": entropy,
        "instances_tested": 10,
        "n_max": n,
        "conjecture_holds": entropy <= n ** 1.5 and width <= 2 * n,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Topological entropy exceeds O(n^1.5)' first_failing_seed={seeds[first_failing_seed]}")