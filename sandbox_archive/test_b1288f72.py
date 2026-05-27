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
    
    def ehrhart_matrix(cnf):
        n = len(cnf)
        matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in cnf:
            for literal in clause:
                row = abs(literal) - 1
                col = literal > 0
                if row < n and col < n + 1:
                    matrix[row][col] += 1
        
        return matrix
    
    def rank(matrix):
        m, n = len(matrix), len(matrix[0])
        augmented_matrix = [row + [Fraction(0)] for row in matrix]
        
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(augmented_matrix[j][i]) > abs(augmented_matrix[max_row][i]):
                    max_row = j
            
            augmented_matrix[i], augmented_matrix[max_row] = augmented_matrix[max_row], augmented_matrix[i]
            
            pivot = augmented_matrix[i][i]
            for j in range(i, n + 1):
                augmented_matrix[i][j] /= pivot
            
            for j in range(m):
                if j != i:
                    factor = augmented_matrix[j][i]
                    for k in range(i, n + 1):
                        augmented_matrix[j][k] -= factor * augmented_matrix[i][k]
        
        rank = sum(1 for row in augmented_matrix if any(row[col] != Fraction(0) for col in range(n)))
        return rank
    
    def generate_cnf(n, density):
        cnf = []
        variables = list(range(1, n + 1))
        
        for _ in range(int(density * n * (n - 1) / 2)):
            clause = [random.choice(variables), random.choice(variables)]
            if len(set(clause)) == 2:
                cnf.append(clause)
        
        return cnf
    
    def read_twice_size(cnf):
        variables = set()
        for clause in cnf:
            for literal in clause:
                variables.add(abs(literal))
        return len(variables)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            density = random.uniform(0.1, 0.9)
            cnf = generate_cnf(n, density)
            matrix = ehrhart_matrix(cnf)
            rank_value = rank(matrix)
            read_twice_n = read_twice_size(cnf)
            
            results.append({
                "n": n,
                "density": density,
                "rank_value": rank_value,
                "read_twice_n": read_twice_n
            })
    
    mean_rank = sum(result["rank_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["rank_value"] <= math.log2(result["read_twice_n"]) ** 2) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_data n_tested={len(seeds)}")