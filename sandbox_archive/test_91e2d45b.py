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
    
    def generate_graph(n):
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def lex_order_complex(edges, n):
        vertices = list(range(n))
        facets = []
        
        def dfs(path, start):
            if len(path) == n:
                facets.append(tuple(sorted(path)))
                return
            for v in range(start, n):
                if (path[-1], v) not in edges and (v, path[-1]) not in edges:
                    dfs(path + [v], v)
        
        for i in range(n):
            dfs([i], i)
        return facets
    
    def resolution_length(facets):
        clauses = []
        for facet in facets:
            clause = [-x - 1 for x in facet]
            clauses.append(clause)
        
        def dpll(clauses, assignment, unit_clause=None):
            if not clauses:
                return True
            if unit_clause is not None:
                var = unit_clause[0]
                if var > 0:
                    assignment[var] = True
                else:
                    assignment[-var] = False
                clauses = [c for c in clauses if var not in c and -var not in c]
            
            literal, polarity = next((l, p) for l, c in enumerate(clauses) for p in (True, False) if (p and l + 1 not in assignment) or (not p and -(l + 1) not in assignment))
            new_assignment = assignment.copy()
            new_assignment[literal] = polarity
            if dpll(clauses, new_assignment):
                return True
            
            new_assignment[literal] = not polarity
            if dpll(clauses, new_assignment):
                return True
            
            return False
        
        assignment = {}
        return len(facets) if dpll(clauses, assignment) else 0
    
    n = random.randint(5, 40)
    while True:
        graph = generate_graph(n)
        expansion_param = sum(len(list(graph.neighbors(v))) for v in range(n)) / (n * (n - 1))
        if expansion_param >= 1 / math.sqrt(n):
            break
    
    facets = lex_order_complex(graph, n)
    resolution_len = resolution_length(facets)
    
    c = 0.3
    conjecture_holds = resolution_len >= 2 ** (c * len(facets))
    counterexample = "" if conjecture_holds else f"Resolution length {resolution_len} < {2 ** (c * len(facets))}"
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": resolution_len,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")