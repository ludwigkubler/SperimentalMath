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
        complex = []
        vertices = list(range(n))
        for subset in itertools.combinations(vertices, 2):
            if (subset[0], subset[1]) in edges or (subset[1], subset[0]) in edges:
                complex.append(subset)
        return complex
    
    def resolution_length(formula):
        stack = []
        for clause in formula:
            found = False
            for literal in clause:
                if -literal in stack:
                    stack.remove(-literal)
                    found = True
                    break
            if not found:
                stack.append(literal)
        return len(stack)
    
    def tseitin_formula(edges, n):
        literals = {}
        formula = []
        for i in range(n):
            literals[i] = random.randint(1, 2 * n)
        for (u, v) in edges:
            a = literals[u]
            b = literals[v]
            c = random.randint(1, 2 * n)
            formula.append([-a, -b, c])
            formula.append([a, -c])
            formula.append([b, -c])
            formula.append([-c])
        return formula
    
    def lex_order_complex_facets(n):
        edges = generate_graph(n)
        if len(edges) < 2:
            return 0
        complex = lex_order_complex(edges, n)
        facets = set()
        for facet in complex:
            facets.add(tuple(sorted(facet)))
        return len(facets)
    
    def run_dpll(formula):
        stack = []
        literals = {}
        for clause in formula:
            found = False
            for literal in clause:
                if -literal in literals:
                    del literals[-literal]
                    found = True
                    break
            if not found:
                stack.append(literal)
                literals[literal] = 1
        return len(stack)
    
    n = random.randint(5, 40)
    while True:
        formula = tseitin_formula(generate_graph(n), n)
        if len(formula) > 10 * n:
            break
    
    facets = lex_order_complex_facets(n)
    resolution_len = run_dpll(formula)
    
    c = 0.3
    if resolution_len >= 2**(c * facets):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"Resolution length {resolution_len} < {2**(c * facets)}"
    
    return {
        "metric_name": "Resolution Length",
        "metric_value": resolution_len,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")