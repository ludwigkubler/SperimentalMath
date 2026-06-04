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
    
    def generate_formula(m, n):
        clauses = []
        for _ in range(m):
            clause = set(random.sample(range(n), 2))
            clauses.append(clause)
        return clauses
    
    def calculate_subset_entropy(clauses):
        num_clauses = len(clauses)
        total_subsets = 1 << num_clauses
        entropy = 0
        for i in range(total_subsets):
            subset = [clauses[j] for j in range(num_clauses) if (i & (1 << j))]
            if subset:
                prob = Fraction(1, total_subsets)
                entropy -= prob * math.log2(prob)
        return entropy
    
    def calculate_minimal_curves(clauses):
        n = len(clauses[0])
        return n * math.log(n)
    
    m = random.randint(5, 30)
    n = random.randint(5, 30)
    clauses = generate_formula(m, n)
    subset_entropy = calculate_subset_entropy(clauses)
    minimal_curves = calculate_minimal_curves(clauses)
    
    return {
        "metric_name": "minimal_curves",
        "metric_value": minimal_curves,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(minimal_curves - m * math.log(n)) <= m * math.log(n) / 2 and abs(subset_entropy - m * math.log(n)) <= m * math.log(n) / 2,
        "counterexample": "" if conjecture_holds else f"m={m}, n={n}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
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
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")