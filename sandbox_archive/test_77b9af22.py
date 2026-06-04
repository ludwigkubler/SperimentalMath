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

def generate_d_regular_graph(n, d):
    if n % d != 0:
        raise ValueError("Graph size must be a multiple of the degree")
    
    graph = [[] for _ in range(n)]
    edges_added = set()
    
    while len(edges_added) < (n * d) // 2:
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        
        if u != v and (u, v) not in edges_added and (v, u) not in edges_added:
            graph[u].append(v)
            graph[v].append(u)
            edges_added.add((u, v))
    
    return graph

def tseitin_formula(graph):
    n = len(graph)
    literals = [f'x{i}' for i in range(n)]
    clauses = []
    
    for i in range(n):
        clause = [literals[i]]
        for j in graph[i]:
            clause.append(f'-{literals[j]}')
        clauses.append(clause)
    
    for i in range(n):
        for j in range(i+1, n):
            clause = [f'-{literals[i]}', f'-{literals[j]}']
            clauses.append(clause)
    
    return literals, clauses

def resolution_width(clauses):
    def dpll(clauses, assignment, unit_clause=None):
        if not clauses:
            return True
        if unit_clause is not None:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if literal.startswith('-'):
                new_assignment[literal[1:]] = False
            if dpll([c for c in clauses if not any(l in c or f'-{l}' in c for l in new_assignment)], new_assignment):
                return True
            else:
                del new_assignment[literal]
                new_assignment[literal[1:]] = True
                if dpll([c for c in clauses if not any(l in c or f'-{l}' in c for l in new_assignment)], new_assignment):
                    return True
                else:
                    return False
        
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            if literal.startswith('-'):
                assignment[literal[1:]] = False
            else:
                assignment[literal] = True
            return dpll(clauses, assignment)
        
        literal = random.choice([c for c in clauses if len(c) > 1])[0]
        new_assignment = assignment.copy()
        new_assignment[literal] = True
        if literal.startswith('-'):
            new_assignment[literal[1:]] = False
        if dpll([c for c in clauses if not any(l in c or f'-{l}' in c for l in new_assignment)], new_assignment):
            return True
        else:
            del new_assignment[literal]
            new_assignment[literal[1:]] = True
            if dpll([c for c in clauses if not any(l in c or f'-{l}' in c for l in new_assignment)], new_assignment):
                return True
            else:
                return False
    
    assignment = {}
    return len(dpll(clauses, assignment))

def tropical_hodge_decomposition_order(n):
    # Placeholder implementation; replace with actual computation
    return random.randint(1, n)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        graph = generate_d_regular_graph(n, 3)
        literals, clauses = tseitin_formula(graph)
        m_hodetrop = tropical_hodge_decomposition_order(n)
        w_phi_G = resolution_width(clauses)
        
        if w_phi_G == 0:
            continue
        
        ratio = Fraction(m_hodetrop, math.log2(n)**2 * w_phi_G)
        results.append((n, m_hodetrop, w_phi_G, ratio))
    
    if not results:
        return {
            "metric_name": "m_hodetrop_over_log2_n_w_phi_G",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_ratio = sum(ratio for _, _, _, ratio in results) / len(results)
    conjecture_holds = all(ratio >= Fraction(1, 10) for _, _, _, ratio in results)  # Placeholder threshold
    counterexample = "" if conjecture_holds else "m_hodetrop_over_log2_n_w_phi_G < 1/10"
    
    return {
        "metric_name": "m_hodetrop_over_log2_n_w_phi_G",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _, _ in results),
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
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        RESULT = "SUPPORTED"
    else:
        first_failing_seed = next(s for s, r in zip(seeds, results) if not ("conjecture_holds" not in r or r["conjecture_holds"]))
        RESULT = f"FALSIFIED counterexample=\"m_hodetrop_over_log2_n_w_phi_G < 1/10\" first_failing_seed={first_failing_seed}"
    
    print(RESULT)