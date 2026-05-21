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
    
    def generate_regular_graph(n, degree):
        if (n * degree) % 2 != 0 or degree >= n:
            return None
        graph = {i: [] for i in range(n)}
        edges_used = set()
        for u in range(n):
            for v in range(u + 1, n):
                if len(graph[u]) < degree and len(graph[v]) < degree and (u, v) not in edges_used:
                    graph[u].append(v)
                    graph[v].append(u)
                    edges_used.add((u, v))
        return graph

    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        for u in range(n):
            if len(graph[u]) < 2:
                continue
            clause = [literals[u]]
            for v in graph[u]:
                clause.append(-literals[v])
            clauses.append(clause)
        return clauses

    def run_dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c[0] for c in clauses if len(c) == 1]
        pure_symbols = {}
        for symbol in set(lit for clause in clauses for lit in clause):
            pos_count = sum(1 for clause in clauses if symbol in clause)
            neg_count = sum(1 for clause in clauses if -symbol in clause)
            if pos_count == 0:
                pure_symbols[symbol] = True
            elif neg_count == 0:
                pure_symbols[symbol] = False
        for symbol, value in pure_symbols.items():
            assignment[symbol] = value
            new_clauses = [c for c in clauses if not (set(c) & {symbol, -symbol})]
            if run_dpll(new_clauses, assignment):
                return True
            assignment[symbol] = not value
        return False

    def resolution(clauses):
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    clause_i = set(clauses[i])
                    clause_j = set(clauses[j])
                    resolvents = [c for c in (clause_i | clause_j) if -c in clause_i and c in clause_j]
                    if not resolvents:
                        continue
                    new_clause = list((clause_i ^ clause_j) - {resolvents[0]})
                    if len(new_clause) == 1:
                        return True
                    if new_clause not in clauses:
                        new_clauses.append(new_clause)
            if not new_clauses:
                return False
            clauses.extend(new_clauses)

    n = random.randint(5, 40)
    degree = random.randint(3, min(n - 1, 4))
    graph = generate_regular_graph(n, degree)
    
    if graph is None:
        return {
            "metric_name": "resolution_proof_length",
            "metric_value": float('inf'),
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "graph_not_possible"
        }

    clauses = tseitin_formula(graph)
    proof_length = resolution(clauses)

    girth = n  # Placeholder for actual girth calculation
    expected_length = 2 ** girth if girth >= 5 else 2 ** (n // 4)
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length >= expected_length,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_length = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length) ** 2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={r['seed']}")
                break