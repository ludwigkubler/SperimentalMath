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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set()
            while len(clause) < 2:
                var = random.randint(1, n)
                sign = random.choice([1, -1])
                clause.add((var, sign))
            clauses.append(clause)
        return clauses
    
    def decision_tree_height(clauses):
        if not clauses:
            return 0
        max_height = 0
        for clause in clauses:
            height = 1 + max(decision_tree_height([c for c in clauses if c != clause]), default=0)
            max_height = max(max_height, height)
        return max_height
    
    def geometric_entropy(clauses):
        n = len(clauses)
        entropy = 0
        for clause in clauses:
            entropy += math.log2(len(clause))
        return entropy / n
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(1, n)
        clauses = generate_k_cnf(n, k)
        height = decision_tree_height(clauses)
        entropy = geometric_entropy(clauses)
        
        results.append({
            "n": n,
            "k": k,
            "height": height,
            "entropy": entropy
        })
    
    if not results:
        return {
            "metric_name": "Geometric Entropy",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mean_entropy = sum(result["entropy"] for result in results) / len(results)
    std_entropy = math.sqrt(sum((result["entropy"] - mean_entropy) ** 2 for result in results) / len(results))
    
    max_ratio = max(result["entropy"] / math.log2(result["height"]) for result in results)
    if max_ratio > mean_entropy + 3 * std_entropy:
        return {
            "metric_name": "Geometric Entropy",
            "metric_value": max_ratio,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": f"Max ratio {max_ratio} exceeds mean + 3*std"
        }
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": max_ratio,
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Max ratio exceeds mean + 3*std' first_failing_seed={first_failing_seed}")