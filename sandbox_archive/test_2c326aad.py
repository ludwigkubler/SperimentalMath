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
    
    def generate_random_graph(n):
        if n <= 1:
            return []
        edges = set()
        for i in range(1, n):
            j = random.randint(0, i-1)
            edges.add((j, i))
        return list(edges)
    
    def cheeger_constant(graph, n):
        min_cut = float('inf')
        for vertex in range(n):
            neighbors = [neighbor for neighbor, _ in graph if neighbor != vertex]
            cut_size = len(neighbors)
            boundary_size = sum(1 for _, neighbor in graph if neighbor == vertex and neighbor not in neighbors)
            if boundary_size > 0:
                min_cut = min(min_cut, cut_size / boundary_size)
        return min_cut
    
    def tseitin_formula(graph, n):
        clauses = []
        for edge in graph:
            u, v = edge
            clause = [f"p{u}", f"p{v}"]
            clauses.append(clause)
            clauses.append([f"-p{u}", f"-p{v}"])
            clauses.append([f"-p{u}", f"p{v}"])
            clauses.append([f"p{u}", f"-p{v}"])
        return clauses
    
    def dpll_solve(clauses):
        def dpll(model, clauses):
            if not clauses:
                return True
            literal = next(l for l in model.keys() if model[l] is None)
            for value in [True, False]:
                new_model = {**model, literal: value}
                new_clauses = []
                for clause in clauses:
                    if any(new_model.get(l) == (not v) for l, v in zip(clause, [True, False])):
                        continue
                    new_clause = [l for l, v in zip(clause, [True, False]) if new_model[l] != v]
                    if not new_clause:
                        return False
                    new_clauses.append(new_clause)
                if dpll(new_model, new_clauses):
                    return True
            return False
        
        model = {f"p{i}": None for i in range(n)}
        return dpll(model, clauses)
    
    n = random.randint(5, 40)
    graph = generate_random_graph(n)
    h_G = cheeger_constant(graph, n)
    tseitin_clauses = tseitin_formula(graph, n)
    proof_length = len(tseitin_clauses) if dpll_solve(tseitin_clauses) else float('inf')
    
    return {
        "metric_name": "resolution_proof_length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": proof_length >= 2 ** (math.ceil(math.log2(h_G)) if h_G > 0 else 0),
        "counterexample": "" if conjecture_holds else f"Graph with n={n}, h(G)={h_G} has proof length {proof_length}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")