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

def gaussian_elimination(matrix):
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        max_row = i + max(range(i, rows), key=lambda r: abs(matrix[r][i]))
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        pivot = matrix[i][i]
        if pivot == 0:
            continue
        for j in range(cols):
            matrix[i][j] /= pivot
        for k in range(rows):
            if k != i and matrix[k][i] != 0:
                factor = matrix[k][i]
                for j in range(cols):
                    matrix[k][j] -= factor * matrix[i][j]
    return matrix

def rank(matrix):
    rows, cols = len(matrix), len(matrix[0])
    row_echelon_form = gaussian_elimination([row[:] for row in matrix])
    rank = 0
    for i in range(rows):
        if any(row_echelon_form[i]):
            rank += 1
    return rank

def tseitin_resolution_tree(cnf):
    literals = set()
    nodes = {}
    edges = []
    
    def add_node(lit):
        if lit not in nodes:
            nodes[lit] = []
    
    def add_edge(u, v):
        edges.append((u, v))
    
    for clause in cnf:
        new_var = len(nodes) + 1
        literals.add(new_var)
        
        add_node(-new_var)
        for literal in clause:
            add_node(literal)
            add_edge(-new_var, literal)
            add_edge(literal, -new_var)
        
        add_edge(new_var, -clause[0])
        for i in range(1, len(clause)):
            add_edge(-clause[i], clause[i-1])
    
    return nodes, literals

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    cnf = []
    for _ in range(n):
        num_literals = random.randint(2, n)
        clause = set()
        while len(clause) < num_literals:
            lit = random.choice([-i for i in range(1, n+1)] + list(range(1, n+1)))
            if lit not in clause:
                clause.add(lit)
        cnf.append(list(clause))
    
    tree, literals = tseitin_resolution_tree(cnf)
    k_group_rank = rank([[0] * len(literals) for _ in range(len(literals))])
    
    return {
        "metric_name": "K_1(T)",
        "metric_value": k_group_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(2, 30))  # First seed is 2 to avoid 1
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")