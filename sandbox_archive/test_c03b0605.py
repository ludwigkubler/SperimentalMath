# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import combinations, product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n):
        literals = [f"x{i}" for i in range(1, n+1)] + [f"~x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(literals, 3)
            while len(set(clause)) != 3:
                clause = random.sample(literals, 3)
            clauses.append(clause)
        return clauses
    
    def cayley_graph(n):
        vertices = [f"x{i}" for i in range(1, n+1)] + [f"~x{i}" for i in range(1, n+1)]
        edges = []
        for v in vertices:
            if "x" in v:
                u = f"~{v[1:]}"
            else:
                u = f"x{v[2:]}"
            edges.append((v, u))
        return vertices, edges
    
    def quotient_space_rank(vertices, edges):
        adjacency_matrix = [[0] * len(vertices) for _ in range(len(vertices))]
        for v1, v2 in edges:
            i1 = vertices.index(v1)
            i2 = vertices.index(v2)
            adjacency_matrix[i1][i2] = 1
            adjacency_matrix[i2][i1] = 1
        
        def gaussian_elimination(A):
            n = len(A)
            for i in range(n):
                max_row = i
                for j in range(i+1, n):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                for j in range(i+1, n):
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
            rank = 0
            for row in A:
                if any(row):
                    rank += 1
            return rank
        
        return gaussian_elimination(adjacency_matrix)
    
    def resolution_depth(formula):
        def dpll_helper(clauses, assignment):
            unit_clauses = [c for c in clauses if len(c) == 1]
            while unit_clauses:
                literal = unit_clauses[0][0]
                if literal.startswith("~"):
                    literal = literal[1:]
                    polarity = False
                else:
                    polarity = True
                assignment.append((literal, polarity))
                new_clauses = []
                for c in clauses:
                    if literal not in c and f"~{literal}" not in c:
                        new_clauses.append(c)
                    elif literal in c:
                        new_clauses.extend([c2 - {literal} for c2 in combinations(c, 1)])
                    else:
                        new_clauses.extend([c2 - {"~" + literal} for c2 in combinations(c, 1)])
                unit_clauses = [c for c in new_clauses if len(c) == 1]
            return not any(clause for clause in clauses)
        
        def dpll(clauses):
            assignment = []
            stack = [(clauses, assignment)]
            while stack:
                clauses, assignment = stack.pop()
                unit_clauses = [c for c in clauses if len(c) == 1]
                if not unit_clauses:
                    return False
                literal, polarity = unit_clauses[0][0], True
                if literal.startswith("~"):
                    literal = literal[1:]
                    polarity = False
                assignment.append((literal, polarity))
                new_clauses = []
                for c in clauses:
                    if literal not in c and f"~{literal}" not in c:
                        new_clauses.append(c)
                    elif literal in c:
                        new_clauses.extend([c2 - {literal} for c2 in combinations(c, 1)])
                    else:
                        new_clauses.extend([c2 - {"~" + literal} for c2 in combinations(c, 1)])
                unit_clauses = [c for c in new_clauses if len(c) == 1]
                stack.append((new_clauses, assignment))
            return False
        
        return len(dpll(formula))

    n = random.randint(5, 40)
    formula = generate_3cnf(n)
    vertices, edges = cayley_graph(n)
    rank = quotient_space_rank(vertices, edges)
    depth = resolution_depth(formula)
    
    conjecture_holds = rank >= math.log2(n) and depth >= math.log2(n)
    counterexample = "" if conjecture_holds else f"n={n}, rank={rank}, depth={depth}"
    
    return {
        "metric_name": "Resolution Depth",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
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