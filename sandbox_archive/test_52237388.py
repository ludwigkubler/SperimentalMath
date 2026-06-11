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
    
    def generate_instance(n):
        literals = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(literals, 3)
            if random.choice([True, False]):
                clause = [-lit for lit in clause]
            clauses.append(clause)
        return literals, clauses
    
    def dpll(instance):
        literals, clauses = instance
        stack = []
        assignment = {}
        
        def solve():
            if not clauses:
                return True
            literal = next(lit for lit in literals if lit not in assignment and -lit not in assignment)
            if literal is None:
                return False
            
            assignment[literal] = True
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            if solve():
                return True
            
            del assignment[literal]
            assignment[-literal] = True
            new_clauses = [c for c in clauses if -literal not in c and literal not in c]
            if solve():
                return True
            
            del assignment[-literal]
            return False
        
        return solve()
    
    def clause_indicator_lattice(instance):
        literals, clauses = instance
        n = len(literals)
        lattice = [[0] * (1 << n) for _ in range(1 << n)]
        
        for i in range(1 << n):
            for j in range(1 << n):
                if all((i & lit == j & lit) or (i & -lit != j & -lit) for lit in range(n)):
                    lattice[i][j] = 1
        
        return lattice
    
    def min_lattice_index(lattice):
        n = len(lattice)
        min_index = float('inf')
        
        for i in range(1 << n):
            for j in range(1 << n):
                if lattice[i][j]:
                    index = sum((i & (1 << k)) != (j & (1 << k)) for k in range(n))
                    if index < min_index:
                        min_index = index
        
        return min_index
    
    def dpll_search_tree_height(instance):
        literals, clauses = instance
        n = len(literals)
        
        def solve(node, assignment):
            if not node:
                return 0
            literal = next(lit for lit in literals if lit not in assignment and -lit not in assignment)
            if literal is None:
                return 0
            
            left = [c for c in clauses if literal not in c and -literal not in c]
            right = [c for c in clauses if -literal not in c and literal not in c]
            
            return max(solve(left, assignment | {literal: True}), solve(right, assignment | {-literal: True})) + 1
        
        return solve(clauses, {})
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_indices = []
    heights = []
    
    for n in n_values:
        instance = generate_instance(n)
        lattice = clause_indicator_lattice(instance)
        min_index = min_lattice_index(lattice)
        height = dpll_search_tree_height(instance)
        
        min_indices.append(min_index)
        heights.append(height)
    
    correlation_coefficient = sum((min_indices[i] - sum(min_indices) / len(min_indices)) * (heights[i] - sum(heights) / len(heights)) for i in range(len(min_indices))) / (len(min_indices) * math.sqrt(sum((min_indices[i] - sum(min_indices) / len(min_indices)) ** 2 for i in range(len(min_indices)))) * math.sqrt(sum((heights[i] - sum(heights) / len(heights)) ** 2 for i in range(len(heights)))))
    mean_absolute_difference = sum(abs(min_indices[i] - heights[i]) for i in range(len(min_indices))) / len(min_indices)
    
    conjecture_holds = correlation_coefficient > 0.8 and mean_absolute_difference <= 3
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}> mean_absolute_difference=<{}>".format(correlation_coefficient, mean_absolute_difference)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_value, std_value, support_fraction))
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(result["counterexample"], first_failing_seed))