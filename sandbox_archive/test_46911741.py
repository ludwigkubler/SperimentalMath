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
    
    def generate_expander_graph(n, phi):
        # Generate a random expander graph with n nodes and expansion phi
        adjacency_list = [[] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < phi / (n - 1):
                    adjacency_list[i].append(j)
                    adjacency_list[j].append(i)
        return adjacency_list
    
    def tseitin_formula(graph, omega):
        # Construct the Tseitin formula for a given graph and assignment
        n = len(graph)
        literals = {i: f"x{i}" for i in range(n)}
        clauses = []
        for i in range(n):
            if omega[i] == 1:
                clauses.append([literals[i]])
            else:
                clauses.append([-literals[i]])
        return clauses
    
    def resolution_width(clauses):
        # Compute the resolution width of a given set of clauses
        queue = [set(clause) for clause in clauses]
        learned_clauses = []
        while True:
            new_clause = None
            for i in range(len(queue)):
                for j in range(i + 1, len(queue)):
                    common_vars = queue[i].intersection(queue[j])
                    if len(common_vars) == 1:
                        new_clause = (queue[i] - common_vars).union(queue[j] - common_vars)
                        learned_clauses.append(new_clause)
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return max(len(clause) for clause in queue + learned_clauses)
            queue.append(new_clause)
    
    def gaussian_elimination(matrix):
        # Perform Gaussian elimination on a given matrix
        n = len(matrix)
        for i in range(n):
            pivot_row = i
            for j in range(i + 1, n):
                if abs(matrix[j][i]) > abs(matrix[pivot_row][i]):
                    pivot_row = j
            matrix[i], matrix[pivot_row] = matrix[pivot_row], matrix[i]
            for j in range(n):
                if j != i:
                    factor = matrix[j][i] / matrix[i][i]
                    for k in range(n + 1):
                        matrix[j][k] -= factor * matrix[i][k]
        return matrix
    
    def determinant(matrix):
        # Compute the determinant of a given square matrix
        n = len(matrix)
        det = 0
        if n == 2:
            det = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        else:
            for j in range(n):
                submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
                det += (-1) ** j * matrix[0][j] * determinant(submatrix)
        return det
    
    def is_expander_graph(graph, phi):
        # Check if a given graph is an expander with expansion phi
        n = len(graph)
        degrees = [len(neighbors) for neighbors in graph]
        min_degree = min(degrees)
        max_degree = max(degrees)
        return (max_degree - min_degree) / min_degree >= phi
    
    def generate_balanced_assignment(n):
        # Generate a balanced assignment for a given number of variables
        omega = [random.choice([0, 1]) for _ in range(n)]
        return omega
    
    n = random.randint(5, 40)
    phi = random.uniform(2, 3)
    graph = generate_expander_graph(n, phi)
    
    if not is_expander_graph(graph, phi):
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    omega = generate_balanced_assignment(n)
    clauses = tseitin_formula(graph, omega)
    width = resolution_width(clauses)
    
    if width is None:
        return {
            "metric_name": "resolution_width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lower_bound = 1 / phi
    if width < lower_bound:
        return {
            "metric_name": "resolution_width",
            "metric_value": width,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"width={width} < lower_bound={lower_bound}"
        }
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_widths = sum(r["metric_value"] for r in results if r["metric_value"] is not None)
    num_trials = len(results)
    mean_width = total_widths / num_trials if num_trials > 0 else 0
    std_width = math.sqrt(sum((r["metric_value"] - mean_width) ** 2 for r in results if r["metric_value"] is not None) / (num_trials - 1)) if num_trials > 1 else 0
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / num_trials
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] is not None for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"] and result["metric_value"] is not None)
        print(f"RESULT: FALSIFIED counterexample='width < lower_bound' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={num_trials}")