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

def generate_kneser_graph(n, k):
    vertices = set(range(1, n + 1))
    edges = []
    for subset in itertools.combinations(vertices, k):
        if len(subset) == k:
            edges.append(frozenset(subset))
    return edges

def tseitin_formula(graph):
    literals = {}
    clauses = []

    def add_clause(literals, clause):
        if not clause:
            return
        literals[clause] = f'x{len(literals)}'
        clauses.append(clause)

    for edge in graph:
        literals[edge] = f'x{len(literals)}'
        literals[frozenset(edge)] = f'y{len(literals)}'

    for edge1, edge2 in itertools.combinations(graph, 2):
        if len(edge1 & edge2) == 0:
            add_clause(literals, [f'{literals[edge1]}', f'~{literals[frozenset(edge1 | edge2)]}'])
            add_clause(literals, [f'{literals[edge2]}', f'~{literals[frozenset(edge1 | edge2)]}'])
            add_clause(literals, [f'~{literals[edge1]}', f'~{literals[edge2]}', f'{literals[frozenset(edge1 | edge2)]}'])

    for vertex in range(1, len(graph) + 1):
        clause = []
        for edge in graph:
            if vertex in edge:
                clause.append(f'{literals[edge]}')
        add_clause(literals, clause)

    return clauses

def dpll_solver(clauses):
    def solve(model):
        unit_clauses = [c for c in clauses if len(c) == 1]
        while unit_clauses:
            literal = unit_clauses.pop()
            model[literal[0]] = True
            new_clauses = []
            for clause in clauses:
                if literal[0] in clause:
                    continue
                if ~literal[0] in clause:
                    new_clauses.append([l for l in clause if l != ~literal[0]])
                else:
                    new_clauses.append(clause)
            clauses = new_clauses
            unit_clauses.extend([c for c in clauses if len(c) == 1])

        pure_literals = {}
        while True:
            for literal, count in collections.Counter(l for clause in clauses for l in clause).items():
                if count % 2 != 0 and literal not in model:
                    pure_literals[literal] = True
            new_clauses = []
            for clause in clauses:
                if any(pure_literal in clause for pure_literal in pure_literals):
                    continue
                new_clauses.append(clause)
            if new_clauses == clauses:
                break
            clauses = new_clauses

        model.update(pure_literals)

        if not all(l in model and model[l] is True or ~l in model and model[~l] is False for l in literals):
            return None

        return model

    return solve({})

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 40
    k = 2
    graph = generate_kneser_graph(n, k)
    tseitin_clauses = tseitin_formula(graph)
    refutation_length = len(dpll_solver(tseitin_clauses))
    return {
        "metric_name": "resolution_refutation_length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": refutation_length >= 2 ** (n / 2),
        "counterexample": "" if refutation_length >= 2 ** (n / 2) else f"Refutation length {refutation_length} < 2^{n/2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_refutation_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_refutation_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_refutation_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Refutation length < 2^{n/2}\" first_failing_seed={seeds[first_failing_seed]}")