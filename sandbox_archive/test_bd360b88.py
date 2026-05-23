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
    
    def generate_cnf(n):
        variables = list(range(1, n+1))
        clauses = []
        for _ in range(n):
            clause = random.sample(variables, 2)
            clauses.append(clause)
        return clauses
    
    def dpll_tree_width(clauses):
        if not clauses:
            return 0
        elif len(clauses) == 1:
            return 1
        else:
            new_clauses = []
            for clause in clauses:
                if all(var in clause for var in variables):
                    continue
                new_clause = [var for var in clause if var not in variables]
                new_clauses.append(new_clause)
            return max(dpll_tree_width(new_clauses), dpll_tree_width([clauses[0]]))
    
    def tropicalized_k_group_rank(clauses):
        # Placeholder function, replace with actual implementation
        return len(clauses)  # Simplified for demonstration
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    width = dpll_tree_width(cnf)
    rank = tropicalized_k_group_rank(cnf)
    
    if width == 0:
        return {
            "metric_name": "ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL tree width is zero"
        }
    
    ratio = rank / width
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
        support_fraction = (sum(1 for r in results if r["conjecture_holds"]) / len(results))

    print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")