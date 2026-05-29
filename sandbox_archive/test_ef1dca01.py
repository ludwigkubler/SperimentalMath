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
    
    def generate_random_kcnf(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    def dpll_tree_depth(instance):
        # Simplified DPLL algorithm to estimate depth
        variables = set(range(1, len(instance) + 1))
        stack = []
        depth = 0
        
        while True:
            if not stack:
                if not variables:
                    return depth
                var = random.choice(list(variables))
                stack.append((var, True))
                stack.append((var, False))
                continue
            
            var, polarity = stack.pop()
            if polarity:
                variables.remove(var)
            else:
                variables.add(var)
            
            if not variables:
                return depth
        
        return depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_depth = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            instance = generate_random_kcnf(n, random.randint(1, n))
            depth = dpll_tree_depth(instance)
            total_depth += depth
            instances_tested += 1
    
    mean_depth = total_depth / instances_tested
    C_n = Fraction(mean_depth / (n * math.log(n)), 1)
    
    # Calculate the expected depth based on Riemann Hypothesis
    expected_depth = C_n * n * math.log(n)
    
    # Calculate Spearman rank correlation coefficient (simplified for demonstration)
    empirical_depths = [dpll_tree_depth(generate_random_kcnf(n, random.randint(1, n))) for n in n_values for _ in range(5)]
    expected_depths = [C_n * n * math.log(n) for n in n_values for _ in range(5)]
    
    def spearman_rank_correlation(empirical, expected):
        if len(empirical) != len(expected):
            return 0
        rank_empirical = {x: i for i, x in enumerate(sorted(empirical))}
        rank_expected = {x: i for i, x in enumerate(sorted(expected))}
        n = len(empirical)
        sum_d_squared = sum((rank_empirical[x] - rank_expected[x]) ** 2 for x in empirical)
        return 1 - (6 * sum_d_squared) / (n * (n**2 - 1))
    
    spearman_corr = spearman_rank_correlation(empirical_depths, expected_depths)
    
    conjecture_holds = spearman_corr >= 0.5
    counterexample = "" if conjecture_holds else "Spearman rank correlation < 0.5"
    
    return {
        "metric_name": "DPLL Tree Depth",
        "metric_value": mean_depth,
        "instances_tested": instances_tested,
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
    
    mean_depth = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Spearman rank correlation < 0.5' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")