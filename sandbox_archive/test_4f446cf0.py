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
from math import log2, ceil

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_formula(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(literals)
        return clauses
    
    def sat_clause_subset_complexity(clauses):
        subsets = []
        for r in range(1, len(clauses) + 1):
            subsets.extend(combinations(clauses, r))
        return len(subsets)
    
    def topological_entropy(tree):
        if not tree:
            return 0
        counts = [sum(1 for node in subtree if node is not None) for subtree in tree]
        probabilities = [count / sum(counts) for count in counts]
        entropy = -sum(p * log2(p) for p in probabilities if p > 0)
        return entropy
    
    def combinations(lst, r):
        if r == 0:
            return [[]]
        result = []
        for i in range(len(lst)):
            rest = lst[i + 1:]
            for c in combinations(rest, r - 1):
                result.append([lst[i]] + c)
        return result
    
    def construct_decision_tree(clauses):
        if not clauses:
            return None
        if len(clauses) == 1:
            return [clauses[0]]
        
        best_entropy = float('inf')
        best_split = None
        
        for i in range(len(clauses)):
            left = construct_decision_tree([c for c in clauses if c[i] > 0])
            right = construct_decision_tree([c for c in clauses if c[i] < 0])
            entropy = topological_entropy([left, right])
            if entropy < best_entropy:
                best_entropy = entropy
                best_split = i
        
        left = construct_decision_tree([c for c in clauses if c[best_split] > 0])
        right = construct_decision_tree([c for c in clauses if c[best_split] < 0])
        return [left, right]
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_entropy = 0
    total_complexity = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_formula(n)
            complexity = sat_clause_subset_complexity(clauses)
            tree = construct_decision_tree(clauses)
            entropy = topological_entropy(tree)
            
            total_entropy += entropy
            total_complexity += complexity
            
            results.append({
                "n": n,
                "entropy": entropy,
                "complexity": complexity
            })
    
    mean_entropy = total_entropy / len(results)
    mean_complexity = total_complexity / len(results)
    correlation_coefficient = sum((r["entropy"] - mean_entropy) * (r["complexity"] - mean_complexity) for r in results) / len(results)
    
    conjecture_holds = abs(correlation_coefficient) >= 0.9
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.9"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")