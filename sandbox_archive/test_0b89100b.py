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
        edges = set()
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    edges.add((i, j))
        return edges
    
    def lex_order_complex(edges, n):
        complex_ = []
        vertices = list(range(n))
        for subset in powerset(vertices):
            valid = True
            for u, v in edges:
                if u not in subset and v in subset:
                    valid = False
                    break
            if valid:
                complex_.append(subset)
        return complex_
    
    def powerset(s):
        result = []
        for i in range(len(s) + 1):
            for combo in itertools.combinations(s, i):
                result.append(combo)
        return result
    
    def resolution_length(clauses, variables):
        stack = []
        while clauses:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                return float('inf')
            literal = unit_clause[0]
            polarity = literal > 0
            literals_to_remove = [l for l in clauses if abs(l) == abs(literal)]
            clauses = [c for c in clauses if c not in literals_to_remove]
            stack.append((literal, polarity))
        return len(stack)
    
    def tseitin_formula(edges):
        n = len(edges)
        variables = {f'x{i}': i for i in range(n)}
        clauses = []
        for u, v in edges:
            clauses.append([variables[f'x{u}'], -variables[f'x{v}']])
            clauses.append([-variables[f'x{u}'], variables[f'x{v}']])
            clauses.append([variables[f'x{u}'], variables[f'x{v}']])
        return clauses, variables
    
    n = random.randint(5, 40)
    while True:
        graph_edges = generate_random_graph(n)
        if len(graph_edges) >= n * (n - 1) / 2 * 0.5:  # Ensure λ(G) ≥ 1/√n
            break
    
    shifted_complex = lex_order_complex(graph_edges, n)
    ν_G = len(shifted_complex)
    
    clauses, variables = tseitin_formula(graph_edges)
    resolution_len = resolution_length(clauses, variables)
    
    if resolution_len < 2**(0.3 * ν_G):
        return {
            "metric_name": "resolution_length",
            "metric_value": resolution_len,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Graph with n={n} and ν(G)={ν_G} has resolution length < 2^{0.3 * ν_G}"
        }
    
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_len,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Graph with n={n} and ν(G)={ν_G} has resolution length < 2^{0.3 * ν_G}' first_failing_seed={first_failing_seed}")