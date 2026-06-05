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

def generate_formula(n):
    clauses = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def construct_decision_tree(clauses):
    if not clauses:
        return "leaf"
    
    counts = {var: 0 for var in set(abs(var) for clause in clauses for var in clause)}
    for clause in clauses:
        for var in clause:
            counts[abs(var)] += 1
    
    decision_var = max(counts, key=counts.get)
    left_clauses = [clause for clause in clauses if decision_var in clause]
    right_clauses = [clause for clause in clauses if -decision_var not in clause]
    
    return {
        "var": decision_var,
        "left": construct_decision_tree(left_clauses),
        "right": construct_decision_tree(right_clauses)
    }

def calculate_topological_entropy(tree):
    if tree == "leaf":
        return 0
    
    left = tree["left"]
    right = tree["right"]
    
    p_left = Fraction(1, 2) * (len(left) / len(clauses))
    p_right = Fraction(1, 2) * (len(right) / len(clauses))
    
    entropy = -p_left * math.log2(p_left) - p_right * math.log2(p_right)
    return entropy

def calculate_clause_subset_complexity(clauses):
    n = len(clauses)
    complexity = sum(1 << i for i in range(n + 1)) - 1
    return complexity

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if instances_tested >= 30:
            break
        
        for _ in range(5):
            clauses = generate_formula(n)
            tree = construct_decision_tree(clauses)
            entropy = calculate_topological_entropy(tree)
            complexity = calculate_clause_subset_complexity(clauses)
            
            metric_values.append((entropy, complexity))
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "Topological Entropy vs Clause Subset Complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_entropy = sum(val[0] for val in metric_values) / len(metric_values)
    mean_complexity = sum(val[1] for val in metric_values) / len(metric_values)
    correlation_coefficient = sum((val[0] - mean_entropy) * (val[1] - mean_complexity) for val in metric_values) / len(metric_values)
    
    return {
        "metric_name": "Topological Entropy vs Clause Subset Complexity",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((res["seed"] for res in results if not res["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_too_low' first_failing_seed={first_failing_seed}")