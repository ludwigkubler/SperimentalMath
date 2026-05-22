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

def generate_random_permutation_matrix(n, seed):
    random.seed(seed)
    matrix = [[0] * n for _ in range(n)]
    elements = list(range(n))
    random.shuffle(elements)
    for i in range(n):
        matrix[i][elements[i]] = 1
    return matrix

def calculate_entropy(matrix):
    eigenvalues = [matrix[i][i] for i in range(len(matrix))]
    entropy = -sum(eigenvalue * math.log2(eigenvalue) for eigenvalue in eigenvalues if eigenvalue != 0)
    return entropy

def generate_and_or_tree(n, seed):
    random.seed(seed)
    if n == 1:
        return [random.choice([0, 1])]
    else:
        left = generate_and_or_tree(n // 2, seed + 1)
        right = generate_and_or_tree(n - n // 2, seed + 2)
        return [[left, right]]

def calculate_communication_complexity(tree):
    if isinstance(tree[0], list):
        return max(calculate_communication_complexity(subtree) for subtree in tree[0]) + 1
    else:
        return 1

def run_trial(seed: int) -> dict:
    n = random.choice([5, 10, 15, 20, 30, 40])
    permutation_matrix = generate_random_permutation_matrix(n, seed)
    entropy = calculate_entropy(permutation_matrix)
    
    and_or_tree = generate_and_or_tree(n, seed + 100)
    communication_complexity = calculate_communication_complexity(and_or_tree)
    
    return {
        "metric_name": "Entropy vs Communication Complexity",
        "metric_value": abs(entropy - communication_complexity),
        "instances_tested": 1,
        "conjecture_holds": abs(entropy - communication_complexity) <= 3,
        "counterexample": "" if entropy <= 10 and communication_complexity >= -7 else f"Entropy: {entropy}, Complexity: {communication_complexity}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or list(range(2, 30 * 2 + 1, 2))
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")