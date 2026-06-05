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
from math import log2

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice([1, -1]) * i for i in range(1, n + 1)]
            clauses.append(literals)
        return clauses
    
    def calculate_clause_subset_complexity(clauses):
        subsets = []
        for r in range(1, len(clauses) + 1):
            for subset in itertools.combinations(clauses, r):
                if all(all(lit in clause for lit in subset) for clause in clauses):
                    subsets.append(subset)
        return len(subsets)
    
    def calculate_topological_entropy(tree):
        counts = [0] * (len(tree) + 1)
        for node in tree:
            counts[len(node)] += 1
        entropy = 0
        total_nodes = sum(counts)
        for count in counts:
            if count > 0:
                probability = count / total_nodes
                entropy -= probability * log2(probability)
        return entropy
    
    def build_decision_tree(clauses):
        tree = []
        stack = [(clauses, [])]
        while stack:
            current_clauses, path = stack.pop()
            if not current_clauses:
                tree.append(path)
                continue
            literal = random.choice(current_clauses[0])
            positive_clauses = [c for c in current_clauses if literal in c]
            negative_clauses = [c for c in current_clauses if -literal in c]
            stack.append((negative_clauses, path + [-1]))
            stack.append((positive_clauses, path + [1]))
        return tree
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_formula(n)
        c_sub = calculate_clause_subset_complexity(formula)
        tree = build_decision_tree(formula)
        h_min = calculate_topological_entropy(tree)
        
        if not (0 < h_min <= log2(2**n)):
            return {
                "metric_name": "topological_entropy",
                "metric_value": h_min,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Invalid entropy value: {h_min}"
            }
        
        results.append({
            "n": n,
            "c_sub": c_sub,
            "h_min": h_min
        })
    
    if len(results) < 30:
        return {
            "metric_name": "topological_entropy",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "Insufficient instances tested"
        }
    
    h_min_values = [result["h_min"] for result in results]
    c_sub_values = [result["c_sub"] for result in results]
    
    mean_h_min = sum(h_min_values) / len(h_min_values)
    std_h_min = (sum((x - mean_h_min) ** 2 for x in h_min_values) / len(h_min_values)) ** 0.5
    
    correlation_coefficient = sum((h_min_values[i] - mean_h_min) * (c_sub_values[i] - mean_c_sub) for i in range(len(h_min_values))) / (len(h_min_values) * std_h_min * std_c_sub)
    
    return {
        "metric_name": "topological_entropy",
        "metric_value": mean_h_min,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": correlation_coefficient >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_h_min = sum(result["metric_value"] for result in results if result["conjecture_holds"]) / len(results)
    std_h_min = (sum((result["metric_value"] - mean_h_min) ** 2 for result in results if result["conjecture_holds"]) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_h_min:.4f} std={std_h_min:.4f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_h_min:.4f} std={std_h_min:.4f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.9\" first_failing_seed={first_failing_seed}")