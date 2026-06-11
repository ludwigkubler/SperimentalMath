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
    
    def generate_formula(n, m):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 3)
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll_search_tree_width(formula):
        def dpll(assignment, literals_left):
            if not literals_left:
                return 1
            literal = literals_left[0]
            positive = literal > 0
            var = abs(literal)
            if var in assignment and (positive == assignment[var]):
                return dpll(assignment, literals_left[1:])
            for val in [True, False]:
                new_assignment = assignment.copy()
                new_assignment[var] = val
                width = dpll(new_assignment, literals_left[1:])
                if width > 0:
                    return width + 1
            return 0
        
        all_literals = set(l for clause in formula for l in clause)
        return max(dpll({}, list(all_literals)), default=1)
    
    def geometric_entropy(formula):
        n = len(formula)
        m = sum(len(clause) for clause in formula)
        width = dpll_search_tree_width(formula)
        
        if width == 0:
            return 0
        
        entropy = 0
        for i in range(1 << n):
            assignment = {j + 1: (i >> j) & 1 for j in range(n)}
            count = sum(1 for clause in formula if all(l in assignment and assignment[l] == (l > 0) for l in clause))
            entropy += math.log2(count / (1 << n))
        
        return entropy
    
    def theta_bound(width):
        return 1.5 ** width / width ** 2
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        m = random.randint(n * 3, n * 6)
        formula = generate_formula(n, m)
        entropy = geometric_entropy(formula)
        bound = theta_bound(dpll_search_tree_width(formula))
        
        results.append({
            "metric_name": "geometric_entropy",
            "metric_value": entropy,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": abs(entropy - bound) <= 0.5 * bound,
            "counterexample": ""
        })
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "geometric_entropy",
        "mean_metric_value": mean,
        "std_metric_value": std,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(result["mean_metric_value"] for result in results) / len(results)
    std_metric_value = math.sqrt(sum((result["mean_metric_value"] - mean_metric_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["support_fraction"] >= 0.8) / len(results)
    
    if all(result["support_fraction"] >= 0.8 for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")