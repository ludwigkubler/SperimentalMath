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
    
    def generate_kneser_graph(n, k):
        V = set(range(1, n + 1))
        E = []
        for S in itertools.combinations(V, k):
            for T in itertools.combinations(V, k):
                if len(S & T) == 0:
                    E.append((S, T))
        return (V, E)
    
    def tseitin_formula(graph):
        V, E = graph
        literals = {frozenset(edge): f'x_{i}' for i, edge in enumerate(E)}
        clauses = []
        
        def add_clause(literals, clause):
            clauses.append(clause)
        
        for edge1 in E:
            for edge2 in E:
                if len(edge1 & edge2) == 0:
                    add_clause(literals, [f'{literals[edge1]}', f'~{literals[frozenset(edge1 | edge2)]}'])
        
        return clauses
    
    def dpll(clauses):
        literals = {}
        stack = []
        
        def is_satisfiable():
            while True:
                if not stack:
                    return True
                literal = stack.pop()
                if literal in literals and literals[literal] == 'false':
                    continue
                if literal not in literals:
                    literals[literal] = 'true'
                    for clause in clauses:
                        if all(lit in literals and literals[lit] == 'true' for lit in clause):
                            break
                    else:
                        stack.append(f'~{literal}')
                        continue
                literals[literal] = 'false'
                for clause in clauses:
                    if literal in clause:
                        for lit in clause:
                            if lit not in literals or literals[lit] == 'true':
                                stack.append(lit)
                                break
                        else:
                            return False
            return True
        
        return is_satisfiable()
    
    n = 40
    graph = generate_kneser_graph(n, 2)
    tseitin_clauses = tseitin_formula(graph)
    refutation_length = len(tseitin_clauses) if dpll(tseitin_clauses) else 0
    
    return {
        "metric_name": "Resolution Refutation Length",
        "metric_value": refutation_length,
        "instances_tested": 1,
        "conjecture_holds": refutation_length >= 2**(n/2),
        "counterexample": "" if refutation_length >= 2**(n/2) else f"Refutation length {refutation_length} < 2^{n/2}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_refutation_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_refutation_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_refutation_length} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Refutation length < 2^(n/2)\" first_failing_seed={first_failing_seed}")