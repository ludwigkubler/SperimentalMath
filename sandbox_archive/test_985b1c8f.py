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
    
    def generate_graph(n):
        edges = set()
        for _ in range(n * (n - 1) // 2):
            u, v = random.sample(range(n), 2)
            if u < v and (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return list(edges)
    
    def tseitin_formula(graph):
        n = len(graph)
        literals = {i: f'x{i}' for i in range(n)}
        clauses = []
        
        # Add clauses for each edge
        for u, v in graph:
            clauses.append([literals[u], literals[v]])
            clauses.append([-literals[u], -literals[v]])
        
        # Add clauses for each vertex
        for i in range(n):
            clauses.append([literals[i]])
            for j in range(i + 1, n):
                clauses.append([-literals[i], -literals[j]])
        
        return clauses
    
    def resolution_proof_depth(clauses):
        stack = []
        while True:
            new_clause = None
            for clause in clauses:
                if len(clause) == 1:
                    literal = clause[0]
                    if literal.startswith('-'):
                        negated_literal = literal[1:]
                        if negated_literal in [c for c in stack]:
                            stack.remove(negated_literal)
                        else:
                            new_clause = [-negated_literal]
                            break
                    elif literal not in stack:
                        stack.append(literal)
                elif len(clause) == 2 and clause[0].startswith('-') and clause[1] == -clause[0][1:]:
                    stack.remove(-clause[0][1:])
            if new_clause is None:
                return len(stack)
    
    def poly_time_invariant(graph):
        n = len(graph)
        # Example invariant: number of edges
        return n * (n - 1) // 2
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    graph = generate_graph(n)
    clauses = tseitin_formula(graph)
    depth = resolution_proof_depth(clauses)
    invariant = poly_time_invariant(graph)
    
    return {
        "metric_name": "Resolution Proof Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": depth >= 2 ** (math.log(n) * math.log(invariant)),
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
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_depth = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_depth} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")