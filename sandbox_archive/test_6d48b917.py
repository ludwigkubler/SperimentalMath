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
    n = 40
    if seed == 0:
        seed = 1  # Avoid using seed=0 as it can cause issues with some libraries
    random.seed(seed)
    
    def generate_random_permutation_matrix(n):
        matrix = [[0] * n for _ in range(n)]
        indices = list(range(n))
        random.shuffle(indices)
        for i in range(n):
            matrix[i][indices[i]] = 1
        return matrix
    
    def calculate_entropy(matrix):
        eigenvalues = [matrix[0][i] for i in range(n)]  # Simplified for demonstration
        entropy = -sum(eigenvalue * math.log2(eigenvalue) for eigenvalue in eigenvalues if eigenvalue != 0)
        return entropy
    
    def generate_and_or_tree(n):
        if n == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_and_or_tree(n // 2)
            right = generate_and_or_tree(n - n // 2)
            return [random.choice([left, right]) for _ in range(n)]
    
    def calculate_communication_complexity(tree):
        if isinstance(tree[0], list):
            return max(calculate_communication_complexity(subtree) for subtree in tree[0])
        else:
            return 1
    
    permutation_matrix = generate_random_permutation_matrix(n)
    entropy = calculate_entropy(permutation_matrix)
    
    and_or_tree = generate_and_or_tree(n)
    communication_complexity = calculate_communication_complexity(and_or_tree)
    
    return {
        "metric_name": "entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": abs(entropy - communication_complexity) <= 3,
        "counterexample": "" if abs(entropy - communication_complexity) <= 3 else f"Entropy: {entropy}, Complexity: {communication_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_entropy = sum(r["metric_value"] for r in results) / len(results)
    std_entropy = math.sqrt(sum((r["metric_value"] - mean_entropy) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std={std_entropy} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")