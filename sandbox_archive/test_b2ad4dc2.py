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
    
    def dpll(instance, assignment=None):
        if assignment is None:
            assignment = {}
        
        # Base case: all literals are assigned
        if len(assignment) == len(instance):
            return True
        
        # Select an unassigned literal
        for lit in instance:
            if lit not in assignment and -lit not in assignment:
                break
        
        # Try assigning the literal
        new_assignment = assignment.copy()
        new_assignment[lit] = True
        if dpll(instance, new_assignment):
            return True
        
        # Try assigning the negation of the literal
        new_assignment[lit] = False
        if dpll(instance, new_assignment):
            return True
        
        return False
    
    def clause_indicator_lattice(clauses):
        n = len(clauses)
        lattice = [[0] * (1 << n) for _ in range(1 << n)]
        
        for i in range(1 << n):
            for j in range(1 << n):
                if all(lit in clauses[i] or -lit in clauses[j] for lit in range(n)):
                    lattice[i][j] = 1
        
        return lattice
    
    def min_lattice_index(lattice):
        n = len(lattice)
        index = 0
        for i in range(1 << n):
            if all(lattice[i][j] == lattice[j][i] for j in range(1 << n)):
                index += 1
        return index
    
    def dpll_search_tree_height(instance, assignment=None):
        if assignment is None:
            assignment = {}
        
        # Base case: all literals are assigned
        if len(assignment) == len(instance):
            return 0
        
        # Select an unassigned literal
        for lit in instance:
            if lit not in assignment and -lit not in assignment:
                break
        
        # Try assigning the literal
        new_assignment = assignment.copy()
        new_assignment[lit] = True
        height_true = dpll_search_tree_height(instance, new_assignment) + 1
        
        # Try assigning the negation of the literal
        new_assignment[lit] = False
        height_false = dpll_search_tree_height(instance, new_assignment) + 1
        
        return max(height_true, height_false)
    
    def generate_random_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(range(-n, n+1), random.randint(1, n))
            clause = [x if x > 0 else -x for x in clause]
            clauses.append(clause)
        return clauses
    
    def correlation_coefficient(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    def mean_absolute_difference(x, y):
        return sum(abs(xi - yi) for xi, yi in zip(x, y)) / len(x)
    
    instance = generate_random_instance(10)
    lattice = clause_indicator_lattice(instance)
    min_ind = min_lattice_index(lattice)
    height = dpll_search_tree_height(instance)
    
    metric_name = "correlation_coefficient"
    metric_value = correlation_coefficient([min_ind], [height])
    instances_tested = 1
    n_max = 10
    conjecture_holds = metric_value > 0.8 and mean_absolute_difference([min_ind], [height]) <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")