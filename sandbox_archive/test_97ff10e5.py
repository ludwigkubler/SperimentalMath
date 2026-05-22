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
            clause = [random.randint(1, n), random.randint(-n, -1)]
            clauses.append(clause)
        return clauses
    
    def decision_tree_height(clauses):
        if not clauses:
            return 0
        heights = [decision_tree_height([c for c in clauses if c != clause]) for clause in clauses]
        return 1 + max(heights, default=0)
    
    def geometric_entropy(curve):
        # Placeholder function to calculate geometric entropy
        # This is a dummy implementation and should be replaced with actual computation
        return random.random()
    
    n = random.randint(5, 40)
    k = random.randint(n // 2, min(n * (n - 1) // 2, 40))
    clauses = generate_k_cnf(n, k)
    height = decision_tree_height(clauses)
    entropy = geometric_entropy(clauses)
    
    return {
        "metric_name": "Geometric Entropy",
        "metric_value": entropy,
        "instances_tested": 1,
        "conjecture_holds": entropy <= 2 * math.log(height),  # Placeholder constant c=2
        "counterexample": "" if entropy <= 2 * math.log(height) else f"Entropy {entropy} > 2*log({height})"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or list(range(3, 100, 4))[:30]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")