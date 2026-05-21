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
        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 0.5:
                    G[i][j] = G[j][i] = 1
        return G
    
    def clique_complex(G):
        n = len(G)
        simplices = []
        for k in range(2, n + 1):
            for subset in itertools.combinations(range(n), k):
                subgraph = [G[i][j] for i in subset for j in subset if i < j]
                if all(subgraph[i * (k - 1) + j] == G[subset[i]][subset[j]] for i in range(k - 1) for j in range(i + 1, k)):
                    simplices.append(subset)
        return simplices
    
    def compute_persistence_barcode(simplices):
        barcode = []
        for s in simplices:
            barcode.append(len(s))
        return sorted(barcode)
    
    def is_expander(G):
        n = len(G)
        degree = [sum(row) for row in G]
        max_degree = max(degree)
        return all(2 * degree[i] >= n - 1 for i in range(n)) and max_degree <= 2 * min(degree)
    
    def dpll_with_timeout(formula, timeout):
        start_time = time.time()
        
        def unit_propagate(clauses, assignment):
            while True:
                changed = False
                for clause in clauses:
                    if len(clause) == 1 and clause[0] not in assignment:
                        assignment[clause[0]] = True
                        changed = True
                    elif len(clause) == 1 and -clause[0] not in assignment:
                        assignment[-clause[0]] = False
                        changed = True
                if not changed:
                    break
        
        def dpll(clauses, assignment):
            unit_propagate(clauses, assignment)
            if not clauses:
                return True
            literal = next(l for l in range(1, len(assignment) + 1) if l not in assignment and -l not in assignment)
            assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], assignment):
                return True
            assignment[literal] = False
            assignment[-literal] = True
            if dpll([c for c in clauses if -literal not in c and literal not in c], assignment):
                return True
            return False
        
        if time.time() - start_time > timeout:
            raise TimeoutError("DPLL timed out")
        
        return dpll(formula, {})
    
    def tseitin_formula(G):
        n = len(G)
        literals = {i: f"x{i+1}" for i in range(n)}
        clauses = []
        for i in range(n):
            clauses.append([literals[i]])
            for j in range(i + 1, n):
                if G[i][j] == 1:
                    clauses.append([f"~{literals[i]}", literals[j]])
                    clauses.append([f"~{literals[j]}", literals[i]])
        return clauses
    
    def resolution_length(clauses):
        start_time = time.time()
        assignment = {}
        while True:
            unit_propagate(clauses, assignment)
            if not clauses:
                return len(assignment) - sum(1 for v in assignment.values() if v is False)
            literal = next(l for l in range(1, len(assignment) + 1) if l not in assignment and -l not in assignment)
            assignment[literal] = True
            if dpll_with_timeout(clauses, timeout=2):
                return len(assignment) - sum(1 for v in assignment.values() if v is False)
            assignment[literal] = False
            assignment[-literal] = True
            if dpll_with_timeout(clauses, timeout=2):
                return len(assignment) - sum(1 for v in assignment.values() if v is False)
        return float('inf')
    
    n = random.randint(5, 40)
    G = generate_graph(n)
    simplices = clique_complex(G)
    barcode = compute_persistence_barcode(simplices)
    ν_G = max(barcode) if barcode else 1
    conjecture_holds = False
    counterexample = ""
    
    if is_expander(G):
        c = 0.2
    else:
        c = 1
    
    try:
        formula = tseitin_formula(G)
        length = resolution_length(formula)
        if length >= 2 ** (c * ν_G):
            conjecture_holds = True
    except TimeoutError:
        counterexample = "DPLL timed out"
    
    return {
        "metric_name": "resolution_length",
        "metric_value": length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    import time
    
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    std_length = math.sqrt(sum((r["metric_value"] - mean_length)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_length} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")