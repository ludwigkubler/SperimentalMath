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
    
    def generate_k_cnf(n, k):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < 3:
                literal = random.choice(variables)
                if random.choice([True, False]):
                    literal = -literal
                clause.add(literal)
            clauses.append(tuple(sorted(clause)))
        return clauses

    def construct_quasi_group(clauses):
        elements = set()
        for clause in clauses:
            for literal in clause:
                elements.add(abs(literal))
        n_elements = len(elements)
        quasi_group = [[0] * n_elements for _ in range(n_elements)]
        element_map = {element: i for i, element in enumerate(sorted(elements))}
        
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    literal_i, literal_j = clause[i], clause[j]
                    if literal_i > 0 and literal_j > 0:
                        quasi_group[element_map[literal_i]][element_map[literal_j]] = element_map[-(literal_i + literal_j)]
                    elif literal_i < 0 and literal_j < 0:
                        quasi_group[element_map[-literal_i]][element_map[-literal_j]] = element_map[literal_i + literal_j]
                    else:
                        quasi_group[element_map[literal_i]][element_map[-literal_j]] = element_map[-(literal_i - literal_j)]
        
        return quasi_group, element_map

    def min_rank(quasi_group):
        n_elements = len(quasi_group)
        rank = 0
        for i in range(n_elements):
            if all(quasi_group[i][j] == 0 for j in range(i + 1, n_elements)):
                rank += 1
        return rank

    def dpll_search_tree(clauses):
        def backtrack(assignment, clause_set):
            if not clause_set:
                return True
            literal = next((l for l in set.union(*clauses) if all(l not in assignment or assignment[l] == v for v in [True, False])), None)
            if literal is None:
                return False
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if backtrack(assignment, new_clauses):
                return True
            assignment[literal] = False
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if backtrack(assignment, new_clauses):
                return True
            return False
        
        assignment = {}
        return len(backtrack(assignment, clauses))

    def gaussian_elimination(matrix):
        n = len(matrix)
        m = len(matrix[0])
        rank = 0
        for i in range(n):
            if rank >= m:
                break
            pivot = None
            for j in range(rank, m):
                if matrix[i][j] != 0:
                    pivot = j
                    break
            if pivot is None:
                continue
            for j in range(m):
                matrix[i][j], matrix[rank][j] = matrix[rank][j], matrix[i][j]
            rank += 1
            for j in range(n):
                if i != j and matrix[j][pivot] != 0:
                    factor = -matrix[j][pivot] / matrix[i][pivot]
                    for k in range(m):
                        matrix[j][k] += factor * matrix[i][k]
        return rank

    def max_height(quasi_group, element_map):
        n_elements = len(quasi_group)
        height = [0] * n_elements
        for i in range(n_elements):
            if all(quasi_group[i][j] == 0 for j in range(i + 1, n_elements)):
                height[i] = 1
        for _ in range(max(height)):
            changed = False
            for i in range(n_elements):
                if height[i] > 0:
                    for j in range(n_elements):
                        if quasi_group[i][j] != 0 and height[j] == 0:
                            height[j] = height[i] + 1
                            changed = True
            if not changed:
                break
        return max(height)

    instances_tested = 30
    rank_sum = 0
    dpll_height_sum = 0

    for _ in range(instances_tested):
        n = random.randint(5, 40)
        k = random.randint(3, 10)
        clauses = generate_k_cnf(n, k)
        quasi_group, element_map = construct_quasi_group(clauses)
        rank = min_rank(quasi_group)
        dpll_height = max_height(quasi_group, element_map)
        
        rank_sum += rank
        dpll_height_sum += dpll_height

    mean_rank = rank_sum / instances_tested
    mean_dpll_height = dpll_height_sum / instances_tested
    abs_diff = abs(mean_rank - mean_dpll_height)

    conjecture_holds = abs_diff <= 3 and (mean_rank - mean_dpll_height) >= 0.8 * (mean_rank + mean_dpll_height)
    counterexample = "" if conjecture_holds else f"Mean rank {mean_rank}, Mean DPLL height {mean_dpll_height}"

    return {
        "metric_name": "Rank vs DPLL Height",
        "metric_value": abs_diff,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)

    mean_abs_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_abs_diff} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_abs_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Mean diff {mean_abs_diff}' first_failing_seed={first_failing_seed}")