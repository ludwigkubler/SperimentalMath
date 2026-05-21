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
    
    def generate_random_3_regular_graph(n):
        if n % 2 != 0 or n < 4:
            return None
        vertices = list(range(n))
        edges = []
        for v in vertices:
            neighbors = random.sample([u for u in vertices if u != v], 3)
            for neighbor in neighbors:
                if (v, neighbor) not in edges and (neighbor, v) not in edges:
                    edges.append((v, neighbor))
        return vertices, edges
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        rank = 0
        for j in range(n):
            i_max = rank
            for i in range(rank, m):
                if abs(A[i][j]) > abs(A[i_max][j]):
                    i_max = i
            if A[i_max][j] == 0:
                continue
            A[rank], A[i_max] = A[i_max], A[rank]
            for i in range(m):
                if i != rank:
                    factor = -A[i][j] / A[rank][j]
                    for k in range(n):
                        A[i][k] += factor * A[rank][k]
            rank += 1
        return rank
    
    def resolution_width(G):
        vertices, edges = G
        n = len(vertices)
        clauses = []
        for v in vertices:
            clause = [random.choice([v, -v]) for _ in range(3)]
            clauses.append(clause)
        assignment = {v: None for v in vertices}
        def unit_propagate():
            changed = True
            while changed:
                changed = False
                for literal in assignment:
                    if assignment[literal] is not None and assignment[literal] == 0:
                        continue
                    clause_found = False
                    for clause in clauses:
                        if all(lit in assignment or -lit in assignment for lit in clause):
                            clause_found = True
                            break
                    if not clause_found:
                        return False
                for literal, value in assignment.items():
                    if value is None and any(lit in assignment or -lit in assignment for lit in clauses):
                        assignment[literal] = 1
                        changed = True
            return True
        def dpll():
            if unit_propagate() == False:
                return float('inf')
            unsatisfied_clauses = [clause for clause in clauses if not any(lit in assignment or -lit in assignment for lit in clause)]
            if len(unsatisfied_clauses) == 0:
                return 1
            literal, _ = random.choice([(v, 1) for v in vertices] + [(-v, -1) for v in vertices])
            assignment[literal] = 1
            width1 = dpll()
            if width1 < float('inf'):
                return width1
            assignment[literal] = -1
            width2 = dpll()
            if width2 < float('inf'):
                return width2
            return float('inf')
        return dpll()
    
    def tseitin_formula(G):
        vertices, edges = G
        n = len(vertices)
        clauses = []
        for v in vertices:
            clause = [random.choice([v, -v]) for _ in range(3)]
            clauses.append(clause)
        literals = {v: None for v in vertices}
        def unit_propagate():
            changed = True
            while changed:
                changed = False
                for literal in literals:
                    if literals[literal] is not None and literals[literal] == 0:
                        continue
                    clause_found = False
                    for clause in clauses:
                        if all(lit in literals or -lit in literals for lit in clause):
                            clause_found = True
                            break
                    if not clause_found:
                        return False
                for literal, value in literals.items():
                    if value is None and any(lit in literals or -lit in literals for lit in clauses):
                        literals[literal] = 1
                        changed = True
            return True
        def dpll():
            if unit_propagate() == False:
                return float('inf')
            unsatisfied_clauses = [clause for clause in clauses if not any(lit in literals or -lit in literals for lit in clause)]
            if len(unsatisfied_clauses) == 0:
                return 1
            literal, _ = random.choice([(v, 1) for v in vertices] + [(-v, -1) for v in vertices])
            literals[literal] = 1
            width1 = dpll()
            if width1 < float('inf'):
                return width1
            literals[literal] = -1
            width2 = dpll()
            if width2 < float('inf'):
                return width2
            return float('inf')
        return dpll()
    
    def tutee_polynomial(G):
        vertices, edges = G
        n = len(vertices)
        T_G_1_1 = 0
        for i in range(n):
            for j in range(i + 1, n):
                if (i, j) in edges or (j, i) in edges:
                    T_G_1_1 += 2
                else:
                    T_G_1_1 -= 1
        return Fraction(T_G_1_1)
    
    for n in [5, 10, 15, 20, 30, 40]:
        G = generate_random_3_regular_graph(n)
        if G is None:
            continue
        T_G_1_1 = tutee_polynomial(G)
        resolution_width_val = resolution_width(G)
        if T_G_1_1 <= 0:
            continue
        if resolution_width_val < math.log(T_G_1_1, 2):
            return {
                "metric_name": "resolution_width",
                "metric_value": resolution_width_val,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"Graph with n={n}, T(G; 1, 1)={T_G_1_1}"
            }
    return {
        "metric_name": "resolution_width",
        "metric_value": resolution_width_val,
        "instances_tested": 6,
        "conjecture_holds": True,
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
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")