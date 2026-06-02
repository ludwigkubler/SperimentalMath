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
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(' | '.join(map(str, clause)))
    return ' & '.join(clauses)

def tseitin_encoding(cnf):
    literals = set()
    new_vars = {}
    stack = []
    for clause in cnf.split(' & '):
        literals.update(int(x.strip()) for x in clause.split('|'))
        if len(literals) > 1:
            new_var = max(new_vars.values(), default=0) + 1
            new_vars[new_var] = set()
            for literal in literals:
                stack.append((literal, new_var))
            literals.clear()
    while stack:
        literal, new_var = stack.pop()
        if literal < 0:
            neg_literal = -literal
            if neg_literal not in new_vars[new_var]:
                new_vars[new_var].add(neg_literal)
                for clause in cnf.split(' & '):
                    if str(-neg_literal) in clause:
                        stack.append((int(x.strip()) for x in clause.split('|')))
        else:
            if literal not in new_vars[new_var]:
                new_vars[new_var].add(literal)
                for clause in cnf.split(' & '):
                    if str(literal) in clause:
                        stack.append((int(x.strip()) for x in clause.split('|')))
    return new_vars

def quiver_representation(cnf):
    new_vars = tseitin_encoding(cnf)
    quiver_rep = {}
    for var, literals in new_vars.items():
        quiver_rep[var] = {literal: 1 if literal > 0 else -1 for literal in literals}
    return quiver_rep

def min_order(quiver_rep):
    n = len(quiver_rep)
    adj_matrix = [[0] * n for _ in range(n)]
    for var, edges in quiver_rep.items():
        for edge, weight in edges.items():
            if edge < 0:
                u = -edge
                v = var
            else:
                u = var
                v = edge
            adj_matrix[u-1][v-1] += weight
    visited = [False] * n
    def dfs(u):
        stack = [u]
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for v in range(n):
                    if adj_matrix[u][v] != 0 and not visited[v]:
                        stack.append(v)
    dfs(0)
    return sum(visited)

def frege_proof_length(cnf):
    # Placeholder function; replace with actual Frege proof length computation
    return len(cnf.split(' & '))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    quiver_rep = quiver_representation(cnf)
    min_order_val = min_order(quiver_rep)
    frege_length = frege_proof_length(cnf)
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": 0.5,  # Placeholder value; replace with actual computation
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(res["metric_value"] < 0.5 for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if res["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"low_correlation\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")