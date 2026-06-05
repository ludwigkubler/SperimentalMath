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
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(variables, 3)
            clauses.append(clause)
        return clauses
    
    def construct_groupoid(clauses):
        groupoid = {}
        for clause in clauses:
            for var in clause:
                if var not in groupoid:
                    groupoid[var] = set()
                for other_var in clause:
                    if other_var != var and other_var not in groupoid[var]:
                        groupoid[var].add(other_var)
        return groupoid
    
    def resolution_width(clauses):
        stack = []
        while clauses:
            new_clause = None
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if set(clauses[i]).isdisjoint(set(clauses[j])):
                        continue
                    common_vars = set(clauses[i]) & set(clauses[j])
                    for var in common_vars:
                        new_clause = [v for v in clauses[i] if v != var] + [v for v in clauses[j] if v != var]
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                return len(stack)
            stack.append(new_clause)
            clauses.remove(new_clause)
        return len(stack)
    
    def min_categorical_dimension(groupoid):
        visited = set()
        dimensions = []
        for var in groupoid:
            if var not in visited:
                queue = [var]
                level = 0
                while queue:
                    next_queue = set()
                    for v in queue:
                        for other_v in groupoid[v]:
                            if other_v not in visited:
                                next_queue.add(other_v)
                                visited.add(other_v)
                    queue = next_queue
                    level += 1
                dimensions.append(level)
        return max(dimensions)
    
    instances_tested = 0
    total_dim = 0
    total_width = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_formula(n)
            groupoid = construct_groupoid(formula)
            dim = min_categorical_dimension(groupoid)
            width = resolution_width(formula)
            total_dim += dim
            total_width += width
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances tested"
        }
    
    mean_dim = total_dim / instances_tested
    mean_width = total_width / instances_tested
    
    if mean_width == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "Division by zero"
        }
    
    correlation_coefficient = (instances_tested * sum(dim * width for dim, width in zip([mean_dim] * instances_tested, [mean_width] * instances_tested)) - 
                                len([dim * width for dim, width in zip([mean_dim] * instances_tested, [mean_width] * instances_tested)]) * mean_dim * mean_width) / \
                               math.sqrt((instances_tested * sum(dim**2 for dim in [mean_dim] * instances_tested) - len([dim] * instances_tested) * mean_dim**2) *
                                         (instances_tested * sum(width**2 for width in [mean_width] * instances_tested) - len([width] * instances_tested) * mean_width**2))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 40,
        "conjecture_holds": correlation_coefficient > 0 and correlation_coefficient < 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = "No seed supported the conjecture"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")