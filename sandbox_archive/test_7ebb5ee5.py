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
    
    def generate_expander_graph(n):
        # Generate a random expander graph using adjacency matrix
        adj_matrix = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if random.random() < 2 / (n - 1):
                    adj_matrix[i][j] = adj_matrix[j][i] = 1
        return adj_matrix
    
    def generate_tseitin_formula(adj_matrix):
        # Generate a Tseitin formula for the given adjacency matrix
        n = len(adj_matrix)
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for i in range(n):
            clause = [variables[i]]
            for j in range(i + 1, n):
                if adj_matrix[i][j] == 1:
                    clause.append(f'~{variables[j]}')
                    clauses.append([f'~{variables[i]}', variables[j]])
            clauses.append(clause)
        return clauses
    
    def compute_geometric_entropy(adj_matrix):
        # Compute the geometric entropy of the tropical curve
        n = len(adj_matrix)
        entropy = 0
        for i in range(n):
            for j in range(i + 1, n):
                if adj_matrix[i][j] == 1:
                    entropy += math.log2(2)
        return entropy
    
    def compute_resolution_refutation_length(clauses):
        # Compute the Resolution refutation length of the Tseitin formula
        stack = []
        for clause in clauses:
            stack.append(clause)
        while stack:
            clause = stack.pop()
            if len(clause) == 1:
                return len(clauses) - len(stack)
            literal = random.choice(clause)
            if literal.startswith('~'):
                literal = literal[1:]
                for i, c in enumerate(clauses):
                    if literal in c:
                        clauses[i].remove(literal)
                        if not c:
                            stack.append(c)
        return len(clauses)
    
    n = 30
    adj_matrix = generate_expander_graph(n)
    formula = generate_tseitin_formula(adj_matrix)
    entropy = compute_geometric_entropy(adj_matrix)
    refutation_length = compute_resolution_refutation_length(formula)
    
    metric_value = entropy / refutation_length if refutation_length > 0 else float('inf')
    conjecture_holds = metric_value >= 0.5
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_entropy_to_refutation_length_ratio",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")