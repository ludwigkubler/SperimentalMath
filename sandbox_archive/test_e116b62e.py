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
        if n == 1:
            return [(0,)]
        edges = []
        for i in range(1, n):
            edges.append((0, i))
        for i in range(1, n-1):
            edges.append((i, i+1))
        edges.append((n-2, n-1))
        random.shuffle(edges)
        return edges
    
    def tseitin_formula(graph):
        literals = {node: f'x_{node}' for node in range(len(graph))}
        clauses = []
        for u, v in graph:
            a = literals[u]
            b = literals[v]
            c = f'x_{len(graph)}'
            clauses.append([a, b, -c])
            clauses.append([-a, c])
            clauses.append([-b, c])
            literals[len(graph)] = c
        return clauses
    
    def resolution_proof_depth(clauses):
        stack = []
        while True:
            new_clause = None
            for clause1 in stack:
                for clause2 in stack:
                    if len(set(clause1) & set(clause2)) == 1:
                        new_clause = [x for x in clause1 + clause2 if x not in set(clause1) & set(clause2)]
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(stack)
            stack.append(new_clause)
    
    def tropicalized_belyi_function(graph):
        n = len(graph)
        belyi_values = {node: 0 for node in range(n)}
        for u, v in graph:
            belyi_values[u] += 1
            belyi_values[v] += 1
        return max(belyi_values.values())
    
    def poly_time_invariant(graph):
        n = len(graph)
        if n == 1:
            return 1
        elif n == 2:
            return 2
        else:
            return n - 1
    
    n = random.randint(5, 40)
    graph = generate_graph(n)
    tseitin_clauses = tseitin_formula(graph)
    resolution_depth = resolution_proof_depth(tseitin_clauses)
    belyi_value = tropicalized_belyi_function(graph)
    invariant_value = poly_time_invariant(graph)
    
    return {
        "metric_name": "Resolution Proof Depth",
        "metric_value": resolution_depth,
        "instances_tested": 1,
        "conjecture_holds": resolution_depth >= 2**(math.log(n) * math.log(invariant_value)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='resolution_depth < 2^(log(n) * log(invariant_value))' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")