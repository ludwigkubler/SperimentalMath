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
    
    # Generate a random quiver with n nodes and m edges
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1))
    quiver = {i: [] for i in range(n)}
    for _ in range(m):
        u, v = random.sample(range(n), 2)
        if v not in quiver[u]:
            quiver[u].append(v)
    
    # Compute the symmetry group of the quiver
    def is_edge(u, v):
        return v in quiver[u]
    
    def compose(g1, g2):
        result = {}
        for u in range(n):
            result[u] = [g2[v] for v in g1[u]]
        return result
    
    def identity():
        return {u: u for u in range(n)}
    
    def inverse(g):
        return {v: u for u, vs in g.items() for v in vs}
    
    def is_group_element(g):
        if len(g) != n:
            return False
        for u in range(n):
            if not all(is_edge(u, v) == is_edge(g[u], g[v]) for v in range(n)):
                return False
        return True
    
    def find_symmetry_group():
        group = [identity()]
        for u in range(n):
            for perm in itertools.permutations(range(n)):
                if all(is_edge(v, w) == is_edge(perm[v], perm[w]) for v, w in quiver[u]):
                    g = {i: perm[i] for i in range(n)}
                    if is_group_element(g):
                        group.append(g)
        return group
    
    symmetry_group = find_symmetry_group()
    
    # Compute the number of conjugacy classes
    def conjugate(g1, g2):
        return compose(inverse(g1), compose(g2, g1))
    
    conjugacy_classes = [symmetry_group[0]]
    for g in symmetry_group:
        if all(not is_equal(conjugate(c, g), c) for c in conjugacy_classes):
            conjugacy_classes.append(g)
    
    def is_equal(g1, g2):
        return all(g1[u] == g2[u] for u in range(n))
    
    num_conjugacy_classes = len(conjugacy_classes)
    
    # Compute the Tseitin formula and resolution refutation length
    variables = {f"x_{u}_{v}" for u in range(n) for v in quiver[u]}
    clauses = []
    for u in range(n):
        if not quiver[u]:
            clauses.append([f"x_{u}_0"])
        else:
            for v in quiver[u]:
                clauses.append([f"x_{u}_{v}"])
    
    def resolve(clauses, literal):
        new_clauses = []
        for clause in clauses:
            if literal in clause:
                continue
            if -literal in clause:
                new_clauses.extend(c for c in clauses if literal not in c and -literal not in c)
                break
            else:
                new_clauses.append([l for l in clause if l != -literal])
        return new_clauses
    
    def is_satisfiable(clauses):
        stack = []
        assignment = {}
        
        def add_clause(clause):
            nonlocal stack, assignment
            for literal in clause:
                if literal < 0 and -literal in assignment:
                    return False
                elif literal > 0 and literal not in assignment:
                    assignment[literal] = True
                    stack.append(literal)
                    break
            else:
                return True
        
        def backtrack():
            nonlocal stack, assignment
            while stack:
                literal = stack.pop()
                if -literal in assignment:
                    del assignment[-literal]
                else:
                    assignment[literal] = False
                    for clause in clauses:
                        if literal in clause and not is_satisfiable([c for c in clauses if literal not in c]):
                            return True
                    break
            return False
        
        for clause in clauses:
            if not add_clause(clause):
                return False
        
        while stack:
            literal = stack.pop()
            if -literal in assignment:
                del assignment[-literal]
            else:
                assignment[literal] = False
                if backtrack():
                    return True
        
        return False
    
    resolution_refutation_length = 0
    while clauses:
        resolution_refutation_length += len(clauses)
        literal = random.choice([l for clause in clauses for l in clause])
        clauses = resolve(clauses, literal)
    
    # Check the conjecture
    if resolution_refutation_length < 2 ** (math.log2(num_conjugacy_classes)):
        return {
            "metric_name": "resolution_refutation_length",
            "metric_value": resolution_refutation_length,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Quiver with {n} nodes and {m} edges, symmetry group with {num_conjugacy_classes} conjugacy classes"
        }
    else:
        return {
            "metric_name": "resolution_refutation_length",
            "metric_value": resolution_refutation_length,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Quiver with {n} nodes and {m} edges, symmetry group with {num_conjugacy_classes} conjugacy classes' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")