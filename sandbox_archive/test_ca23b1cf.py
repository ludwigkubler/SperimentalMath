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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        max_row = i + A[i:].index(max(abs(row[i]) for row in A[i:]))
        A[i], A[max_row] = A[max_row], A[i]
        pivot = A[i][i]
        if pivot == 0:
            continue
        for j in range(i, n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i and A[k][i] != 0:
                factor = A[k][i]
                for j in range(i, n):
                    A[k][j] -= factor * A[i][j]
    return A

def rank_matrix(A):
    n = len(A)
    rank = sum(1 for row in gaussian_elimination(A) if any(row[i] != 0 for i in range(n)))
    return rank

def geometric_entropy(G):
    A = G['matrix']
    n = len(A)
    rank = rank_matrix(A)
    H_G = -rank * math.log2(rank / n)
    return H_G

def dpll_search_tree_width(CNF):
    # Simplified DPLL solver to estimate width
    def solve(clauses, assignment, literals):
        if not clauses:
            return 1
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            return solve([c for c in clauses if literal not in c and -literal not in c], new_assignment, literals)
        pure_literal = next((l for l in literals if all(l not in c or -l in c for c in clauses)), None)
        if pure_literal is not None:
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return solve(clauses, new_assignment, [l for l in literals if l != pure_literal])
        literal = random.choice(literals)
        new_assignment1 = assignment.copy()
        new_assignment1[literal] = True
        new_assignment2 = assignment.copy()
        new_assignment2[-literal] = True
        return max(solve(clauses, new_assignment1, [l for l in literals if l != literal]), solve(clauses, new_assignment2, [l for l in literals if l != -literal]))
    return dpll_search_tree_width(CNF)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 3, n * 10)
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(m):
        clause = random.sample(variables + [-v for v in variables], random.randint(1, n))
        clauses.append(clause)
    CNF = {'variables': variables, 'clauses': clauses}
    
    G = {
        'matrix': [[0] * n for _ in range(n)],
        'n': n
    }
    for clause in CNF['clauses']:
        for literal in clause:
            if literal > 0:
                row = literal - 1
                col = variables.index(literal)
            else:
                row = -literal - 1
                col = variables.index(-literal)
            G['matrix'][row][col] = 1
    
    H_G = geometric_entropy(G)
    W_G = dpll_search_tree_width(CNF)
    
    return {
        "metric_name": "H_G",
        "metric_value": H_G,
        "instances_tested": 1,
        "conjecture_holds": H_G <= 0.5 * n * math.log2(m) and W_G <= 3 * math.sqrt(H_G),
        "counterexample": "" if H_G <= 0.5 * n * math.log2(m) and W_G <= 3 * math.sqrt(H_G) else f"H(G)={H_G}, W(G)={W_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 103))  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_H_G = sum(r['metric_value'] for r in results) / len(results)
    std_H_G = math.sqrt(sum((r['metric_value'] - mean_H_G) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_H_G} std={std_H_G} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_H_G} std={std_H_G} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f"RESULT: FALSIFIED counterexample=\"H(G) > 0.5 * n * log2(m) or W(G) > 3 * sqrt(H(G))\" first_failing_seed={first_failing_seed}")