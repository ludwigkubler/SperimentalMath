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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if any(abs(clause[i]) == abs(clause[j]) for i in range(n) for j in range(i+1, n)):
                continue
            clauses.append(clause)
        return clauses

    def incidence_complex(cnf):
        vertices = set()
        edges = []
        for clause in cnf:
            for literal in clause:
                vertices.add(abs(literal))
            for i in range(len(clause)):
                for j in range(i+1, len(clause)):
                    if (abs(clause[i]), abs(clause[j])) not in edges and (abs(clause[j]), abs(clause[i])) not in edges:
                        edges.append((abs(clause[i]), abs(clause[j])))
        return vertices, edges

    def gromov_distortion(vertices, edges):
        n = len(vertices)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for u, v in edges:
            adjacency_matrix[u-1][v-1] = 1
            adjacency_matrix[v-1][u-1] = 1
        
        def gaussian_elimination(A):
            m, n = len(A), len(A[0])
            for i in range(m):
                max_row = i
                for j in range(i+1, m):
                    if abs(A[j][i]) > abs(A[max_row][i]):
                        max_row = j
                A[i], A[max_row] = A[max_row], A[i]
                for j in range(i+1, m):
                    factor = A[j][i] / A[i][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
            return A
        
        def norm(A):
            n = len(A)
            max_norm = 0
            for i in range(n):
                row_sum = sum(abs(A[i][j]) for j in range(n))
                if row_sum > max_norm:
                    max_norm = row_sum
            return max_norm
        
        A = gaussian_elimination(adjacency_matrix)
        distortion = norm(A) / n
        return distortion

    def dpll_search_tree_height(cnf):
        def backtrack(assignment, clause_indices):
            if not clause_indices:
                return 0
            literal = cnf[clause_indices[0]][0]
            if literal in assignment and assignment[literal] != 1:
                return backtrack(assignment, clause_indices[1:])
            new_assignment = assignment.copy()
            new_assignment[literal] = 1
            if all(any(lit not in assignment or assignment[lit] == -1 for lit in clause) for clause in cnf):
                return 1 + backtrack(new_assignment, clause_indices[1:])
            new_assignment[literal] = -1
            if all(any(lit not in assignment or assignment[lit] == 1 for lit in clause) for clause in cnf):
                return 1 + backtrack(new_assignment, clause_indices[1:])
            return max(1 + backtrack(new_assignment, clause_indices[1:]), 1 + backtrack(new_assignment, clause_indices[1:]))

        return backtrack({}, list(range(len(cnf))))

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    vertices, edges = incidence_complex(cnf)
    distortion = gromov_distortion(vertices, edges)
    height = dpll_search_tree_height(cnf)

    if distortion <= 0 or height <= 0:
        return {
            "metric_name": "distortion",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "invalid_distortion_or_height"
        }

    log_n = math.log(n)
    distortion_bound = 2 * log_n
    height_bound = (0.5, 1.5) * log_n

    conjecture_holds = distortion <= distortion_bound and height >= height_bound[0] and height <= height_bound[1]
    counterexample = "" if conjecture_holds else "distortion={:.2f}, height={}".format(distortion, height)

    return {
        "metric_name": "distortion",
        "metric_value": distortion,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", result)
        results.append(result)

    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)

    if all(res["conjecture_holds"] for res in results):
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.4f} std={:.4f} support_fraction={:.2f}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))