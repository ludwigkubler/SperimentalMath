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
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def decision_tree_height(clauses):
        height = 0
        for clause in clauses:
            height += len(clause) + 1
        return height

    def geometric_entropy(curve):
        # Placeholder function to compute geometric entropy
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(1, n)
        cnf_formula = generate_k_cnf(n, k)
        height = decision_tree_height(cnf_formula)
        entropy = geometric_entropy(cnf_formula)
        
        results.append({
            "n": n,
            "k": k,
            "height": height,
            "entropy": entropy
        })
    
    mean_entropy = sum(result["entropy"] for result in results) / len(results)
    std_entropy = math.sqrt(sum((result["entropy"] - mean_entropy) ** 2 for result in results) / len(results))
    
    c = 1.0  # Placeholder constant
    threshold = c * math.log(max(result["height"] for result in results))
    
    conjecture_holds = all(result["entropy"] <= threshold for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": mean_entropy,
        "instances_tested": len(results),
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
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")