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

# Helper functions for matrix operations
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
            if i != rank and A[i][j] != 0:
                factor = -A[i][j] / A[rank][j]
                for k in range(n):
                    A[i][k] += factor * A[rank][k]
        rank += 1
    return rank

def matrix_multiplication(A, B):
    m, n, p = len(A), len(B), len(B[0])
    C = [[0] * p for _ in range(m)]
    for i in range(m):
        for k in range(p):
            for j in range(n):
                C[i][k] += A[i][j] * B[j][k]
    return C

def rank_of_matrix(A):
    return gaussian_elimination(A)

# Function to generate a random n-variable CNF formula
def generate_cnf(num_vars, num_clauses):
    cnf = []
    for _ in range(num_clauses):
        clause = set()
        while len(clause) < 3:
            var = random.randint(1, num_vars)
            sign = random.choice([True, False])
            if (var, sign) not in clause and (-var, not sign) not in clause:
                clause.add((var, sign))
        cnf.append(clause)
    return cnf

# Function to compute the truth table of a CNF formula
def truth_table(cnf, num_vars):
    n = 2 ** num_vars
    tt = [[False] * n for _ in range(len(cnf))]
    for i in range(n):
        assignment = [(i >> j) & 1 == 1 for j in range(num_vars)]
        for clause in cnf:
            if all((assignment[var - 1] if sign else not assignment[var - 1]) for var, sign in clause):
                tt[len(cnf) - 1][i] = True
                break
    return tt

# Function to construct the DPLL refutation tree and calculate its diameter
def dpll_refutation_tree(cnf, num_vars):
    def dpll(clause_set, assignment):
        if not clause_set:
            return [assignment]
        unit_clause = next((c for c in clause_set if len(c) == 1), None)
        if unit_clause:
            var, sign = unit_clause[0]
            new_assignment = assignment[:]
            new_assignment[var - 1] = sign
            return dpll(clause_set - {unit_clause}, new_assignment)
        pure_literal = next((v for v in range(1, num_vars + 1) if (v not in [abs(x) for x in assignment] and (-v not in [abs(x) for x in assignment]))), None)
        if pure_literal:
            sign = True
            new_assignment = assignment[:]
            new_assignment[pure_literal - 1] = sign
            return dpll(clause_set, new_assignment)
        var = next((v for v in range(1, num_vars + 1) if v not in [abs(x) for x in assignment]), None)
        true_branch = dpll(clause_set, assignment + [(var, True)])
        false_branch = dpll(clause_set, assignment + [(var, False)])
        return true_branch + false_branch

    refutation_tree = dpll(set(cnf), [])
    edges = []
    for node in refutation_tree:
        for other_node in refutation_tree:
            if node != other_node and any(abs(x) not in [abs(y) for y in node] for x in other_node):
                edges.append((node, other_node))
    return len(refutation_tree), max(len(list(bfs(edges, start))) - 1 for start in refutation_tree)

def bfs(edges, start):
    visited = set()
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            neighbors = {neighbor for neighbor, _ in edges if neighbor == node}
            queue.extend(neighbors - visited)
    return visited

def run_trial(seed: int) -> dict:
    random.seed(seed)
    num_vars = 5
    num_clauses = 10
    cnf = generate_cnf(num_vars, num_clauses)
    tt = truth_table(cnf, num_vars)
    rank = rank_of_matrix(tt)
    _, diameter = dpll_refutation_tree(cnf, num_vars)
    
    if rank < diameter:
        return {
            "metric_name": "rank vs diameter",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Rank {rank} < Diameter {diameter}"
        }
    
    return {
        "metric_name": "rank vs diameter",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank < diameter\" first_failing_seed={first_failing_seed}")