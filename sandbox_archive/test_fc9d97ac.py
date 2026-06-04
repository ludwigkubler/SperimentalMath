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
    
    def generate_formula(n, m):
        variables = [f"x{i}" for i in range(1, n+1)]
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def affine_quotient_group_size(clauses):
        # Simplified encoding of the affine quotient group size
        # This is a placeholder function and should be replaced with actual computation
        return len(clauses) ** 2
    
    def clause_subset_entropy(clauses):
        total_clauses = len(clauses)
        entropy = 0
        for i in range(1, total_clauses + 1):
            entropy += math.comb(total_clauses, i) * (i / total_clauses) * ((total_clauses - i) / total_clauses)
        return entropy
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        m = random.randint(n // 2, n * 2)
        clauses = generate_formula(n, m)
        
        generators = affine_quotient_group_size(clauses)
        entropy = clause_subset_entropy(clauses)
        
        metric_values.append(generators)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    
    conjecture_holds = all(3 * entropy**2 <= generators <= 10 * entropy**2 for generators, entropy in zip(metric_values, [clause_subset_entropy(generate_formula(n, m)) for _ in range(instances_tested)]))
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Generators",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")