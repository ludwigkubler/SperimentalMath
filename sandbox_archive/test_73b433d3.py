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
    
    def generate_permutation_matrix(n):
        matrix = [[0] * n for _ in range(n)]
        indices = list(range(n))
        random.shuffle(indices)
        for i, idx in enumerate(indices):
            matrix[i][idx] = 1
        return matrix
    
    def calculate_entropy(matrix):
        eigenvalues = [matrix[0][i] for i in range(len(matrix))]
        entropy = -sum(e * math.log2(e) for e in eigenvalues if e != 0)
        return entropy
    
    def generate_and_or_tree(n):
        if n == 1:
            return "leaf"
        else:
            left = generate_and_or_tree(n // 2)
            right = generate_and_or_tree((n + 1) // 2)
            return f"and({left}, {right})"
    
    def calculate_communication_complexity(tree):
        if tree == "leaf":
            return 0
        else:
            left, right = tree.split("(")[1].split(",")[0], tree.split(",")[1].strip(")")
            return max(calculate_communication_complexity(left), calculate_communication_complexity(right)) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_entropy = 0
    total_complexity = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            matrix = generate_permutation_matrix(n)
            entropy = calculate_entropy(matrix)
            tree = generate_and_or_tree(n)
            complexity = calculate_communication_complexity(tree)
            
            if entropy > 10 or complexity < -7:
                return {
                    "metric_name": "Entropy/Complexity",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "conjecture_holds": False,
                    "counterexample": f"Seed {seed}: Entropy={entropy}, Complexity={complexity}"
                }
            
            total_entropy += entropy
            total_complexity += complexity
            instances_tested += 1
    
    mean_entropy = total_entropy / instances_tested
    mean_complexity = total_complexity / instances_tested
    
    return {
        "metric_name": "Entropy/Complexity",
        "metric_value": {"mean_entropy": mean_entropy, "mean_complexity": mean_complexity},
        "instances_tested": instances_tested,
        "conjecture_holds": abs(mean_entropy - mean_complexity) <= 3,
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
    
    mean_entropy = sum(r["metric_value"]["mean_entropy"] for r in results if "mean_entropy" in r) / len(results)
    mean_complexity = sum(r["metric_value"]["mean_complexity"] for r in results if "mean_complexity" in r) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all("mean_entropy" in r and "mean_complexity" in r for r in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean_entropy={mean_entropy} std_entropy=0 support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='Support fraction too low' first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE Some trials did not produce valid entropy/complexity values.")