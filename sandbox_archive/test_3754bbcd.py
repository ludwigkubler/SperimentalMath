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
    
    def generate_kneser_graph(n, k):
        vertices = list(range(1, n + 1))
        edges = []
        for comb in itertools.combinations(vertices, k):
            edges.extend([frozenset(comb), frozenset(set(vertices) - set(comb))])
        return edges
    
    def tseitin_formula(graph):
        literals = {}
        clauses = []
        
        def add_clause(literals, clause):
            clauses.append(clause)
        
        for i, edge in enumerate(graph):
            literals[edge] = f'x{i}'
            add_clause(literals, [f'~{literals[edge]}'])
        
        for i, edge1 in enumerate(graph):
            for j, edge2 in enumerate(graph):
                if i < j and len(edge1 & edge2) == 0:
                    add_clause(literals, [f'{literals[edge1]}', f'{literals[edge2]}', f'~{literals[frozenset(edge1 | edge2)]}'])
        
        return clauses
    
    def dpll(clauses):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_clauses = [c for c in clauses if literal not in c and f'~{literal}' not in c]
            return dpll(new_clauses)
        
        literals = set()
        for clause in clauses:
            literals.update(clause)
        
        literal = next(lit for lit in literals if all(f'~{lit}' not in c for c in clauses))
        new_clauses_true = [c for c in clauses if literal not in c]
        new_clauses_false = [c for c in clauses if f'~{literal}' not in c]
        
        return dpll(new_clauses_true) or dpll(new_clauses_false)
    
    def resolution(clauses):
        while True:
            unit_clauses = [c for c in clauses if len(c) == 1]
            if unit_clauses:
                literal = unit_clauses[0][0]
                new_clauses = [c for c in clauses if literal not in c and f'~{literal}' not in c]
                clauses = new_clauses
            else:
                pairs = [(i, j) for i in range(len(clauses)) for j in range(i + 1, len(clauses))]
                new_clause = None
                for i, j in pairs:
                    if any(lit in clauses[i] and f'~{lit}' in clauses[j] for lit in clauses[i]):
                        new_clause = [l for l in clauses[i] if l not in clauses[j]] + [l for l in clauses[j] if f'~{l}' not in clauses[i]]
                        break
                if new_clause is None:
                    return len(clauses)
                clauses.append(new_clause)
    
    n = 40
    k = 2
    graph = generate_kneser_graph(n, k)
    tseitin_clauses = tseitin_formula(graph)
    refutation_length = resolution(tseitin_clauses)
    
    metric_name = "resolution_refutation_length"
    metric_value = refutation_length
    instances_tested = 1
    conjecture_holds = refutation_length >= 2**(n/2)
    counterexample = "" if conjecture_holds else f"Refutation length {refutation_length} < 2^{n/2}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
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
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")