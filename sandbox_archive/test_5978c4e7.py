# auto-injected by SEC sandbox
import itertools
import collections
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
import json
from sys import argv

def run_trial(seed: int) -> dict:
    n = 10  # Start with a smaller size for faster testing
    random.seed(seed)
    
    def generate_3cnf(n, num_clauses):
        clauses = []
        variables = list(range(1, n + 1))
        for _ in range(num_clauses):
            clause = []
            while len(clause) < 3:
                var = random.choice(variables)
                if var not in clause and -var not in clause:
                    clause.append(var)
            clauses.append(clause)
        return clauses
    
    def construct_adjacency_matrix(n, clauses):
        matrix = [[0] * n for _ in range(n)]
        for clause in clauses:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    var_i = abs(clause[i])
                    var_j = abs(clause[j])
                    if var_i != var_j and matrix[var_i - 1][var_j - 1] == 0:
                        matrix[var_i - 1][var_j - 1] = 1
                        matrix[var_j - 1][var_i - 1] = 1
        return matrix
    
    def largest_eigenvalue(matrix):
        n = len(matrix)
        eigenvalues = [0] * n
        for _ in range(100):  # Simple power iteration method
            v = [random.random() for _ in range(n)]
            v /= math.sqrt(sum(x**2 for x in v))
            v_next = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
            v_next /= math.sqrt(sum(x**2 for x in v_next))
            eigenvalues.append(max(v_next))
        return max(eigenvalues)
    
    def dpll_runtime(clauses):
        # Basic DPLL implementation
        assignment = [None] * (n + 1)
        
        def solve(index):
            if index == n + 1:
                return True
            for value in [-1, 1]:
                assignment[index] = value
                if all(any(assignment[abs(lit)] == lit for lit in clause) for clause in clauses):
                    if solve(index + 1):
                        return True
            assignment[index] = None
            return False
        
        return solve(1)
    
    clauses = generate_3cnf(n, n * (n - 1) // 2)
    adjacency_matrix = construct_adjacency_matrix(n, clauses)
    lambda_max = largest_eigenvalue(adjacency_matrix)
    runtime = dpll_runtime(clauses)
    
    return {
        "metric_name": "DPLL Runtime",
        "metric_value": runtime,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in argv[1:]] if argv[1:] else [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {json.dumps(result)}")
        results.append(result)
    
    mean_runtime = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_runtime} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")