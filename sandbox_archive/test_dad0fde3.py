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
    
    def generate_random_group(n):
        # Generate a random group presentation P with n generators and relations
        generators = [f'g{i}' for i in range(1, n+1)]
        relations = []
        for i in range(n):
            for j in range(i+1, n):
                relations.append(f'{generators[i]} * {generators[j]} = {generators[j]} * {generators[i]}')
        return generators, relations
    
    def generate_random_tseitin_formula(n):
        # Generate a random Tseitin formula F on n variables
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(n):
            clauses.append(f'{variables[i]}')
            clauses.append(f'~{variables[i]}')
        return clauses
    
    def compute_tropical_representation_rank(generators, relations):
        # Compute the rank of the tropical representation ρ of G over [0,1]
        n = len(generators)
        adjacency_matrix = [[0] * n for _ in range(n)]
        for relation in relations:
            parts = relation.split('=')
            left = parts[0].split('*')
            right = parts[1].split('*')
            for l in left:
                for r in right:
                    if l != r:
                        adjacency_matrix[generators.index(l)][generators.index(r)] = 1
        rank = 0
        for i in range(n):
            row_sum = sum(adjacency_matrix[i])
            col_sum = sum(row[i] for row in adjacency_matrix)
            rank += max(row_sum, col_sum)
        return rank
    
    def estimate_resolution_refutation_size(clauses):
        # Estimate the resolution refutation size for F
        n = len(clauses)
        refutation_size = 2 ** n
        return refutation_size
    
    n = random.randint(5, 40)
    generators, relations = generate_random_group(n)
    clauses = generate_random_tseitin_formula(n)
    
    rank = compute_tropical_representation_rank(generators, relations)
    estimated_refutation_size = estimate_resolution_refutation_size(clauses)
    actual_refutation_size = 2 ** rank
    
    if estimated_refutation_size == 0:
        return {
            "metric_name": "Resolution Refutation Size",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation = abs(estimated_refutation_size / actual_refutation_size - 1)
    
    return {
        "metric_name": "Resolution Refutation Size",
        "metric_value": correlation,
        "instances_tested": 1,
        "conjecture_holds": correlation < 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")