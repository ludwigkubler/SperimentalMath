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
    
    def generate_cnf(num_vars, num_clauses):
        cnf = []
        for _ in range(num_clauses):
            clause = [random.randint(1, num_vars), -random.randint(1, num_vars)]
            cnf.append(clause)
        return cnf
    
    def binary_tree(cnf):
        if not cnf:
            return None
        root = (cnf[0][0], cnf[0][1])
        left_cnf = [c for c in cnf if c[0] == root[0]]
        right_cnf = [c for c in cnf if c[1] == root[1]]
        return (root, binary_tree(left_cnf), binary_tree(right_cnf))
    
    def geometric_entropy(tree):
        if not tree:
            return 0
        root, left, right = tree
        entropy = 1 + geometric_entropy(left) + geometric_entropy(right)
        return entropy
    
    def circuit_depth(cnf):
        if not cnf:
            return 0
        depth = 1
        for clause in cnf:
            depth = max(depth, max(abs(clause[0]), abs(clause[1])))
        return depth
    
    n_max = 40
    instances_tested = 0
    metric_values = []
    
    for n in range(5, n_max + 1):
        for _ in range(6):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2 * n, 4 * n))
            tree = binary_tree(cnf)
            entropy = geometric_entropy(tree)
            depth = circuit_depth(cnf)
            metric_values.append((entropy, depth))
            instances_tested += 1
    
    if not metric_values:
        return {
            "metric_name": "geometric_entropy",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entropy_values, depth_values = zip(*metric_values)
    mean_entropy = sum(entropy_values) / len(entropy_values)
    mean_depth = sum(depth_values) / len(depth_values)
    std_dev = math.sqrt(sum((x - mean_depth) ** 2 for x in depth_values) / len(depth_values))
    
    support_fraction = sum(abs(x - y) <= 3 * std_dev for x, y in zip(entropy_values, depth_values)) / len(entropy_values)
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_depth,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")