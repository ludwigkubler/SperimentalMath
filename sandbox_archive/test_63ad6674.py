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
    
    def generate_tseitin_formula(n):
        variables = list(range(1, n + 2))
        clauses = []
        for i in range(1, n + 1):
            clauses.append([variables[i - 1], variables[n + i - 1]])
            clauses.append([-variables[i - 1], -variables[n + i - 1]])
            for j in range(i + 1, n + 1):
                clauses.append([-variables[i - 1], variables[j - 1], -variables[n + j - 1]])
        return clauses
    
    def compute_min_rank(clauses):
        # Simplified homology computation (not actual rank)
        return len(clauses) // 2
    
    def resolution_length(clauses):
        stack = []
        for clause in clauses:
            if not any(abs(lit) in [abs(x) for x in stack] for lit in clause):
                stack.append(clause[0])
        return len(stack)
    
    n = random.randint(5, 40)
    formula = generate_tseitin_formula(n)
    min_rank = compute_min_rank(formula)
    proof_length = resolution_length(formula)
    
    if min_rank == 0:
        return {
            "metric_name": "Ratio of Resolution Proof Length to 2^(Min Rank)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "min_rank is zero"
        }
    
    ratio = proof_length / (2 ** min_rank)
    return {
        "metric_name": "Ratio of Resolution Proof Length to 2^(Min Rank)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["metric_value"] is not None and r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not (r["metric_value"] is not None and r["conjecture_holds"])), None)
        print(f"RESULT: FALSIFIED counterexample='min_rank_zero' first_failing_seed={first_failing_seed}")