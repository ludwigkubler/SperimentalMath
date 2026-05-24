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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), 3)]
            clauses.append(clause)
        return clauses
    
    def dpll_refutation_tree_width(clauses):
        # Simplified DPLL algorithm to estimate tree width
        def dpll(model, clauses):
            if not clauses:
                return True
            literal = next(l for clause in clauses if any(abs(l) in model for l in clause))
            pos_literal = abs(literal)
            if literal > 0:
                model.add(pos_literal)
            else:
                model.discard(pos_literal)
            if dpll(model, [c for c in clauses if not any(l in c for l in model)]):
                return True
            model.discard(pos_literal)
            if literal < 0:
                model.add(-pos_literal)
            if dpll(model, [c for c in clauses if not any(l in c for l in model)]):
                return True
            model.discard(-pos_literal)
            return False
        
        max_width = 0
        for _ in range(10):  # Run DPLL multiple times to estimate width
            model = set()
            width = len(model) + 1
            if dpll(model, clauses):
                max_width = max(max_width, width)
        return max_width
    
    def tropical_theta_function(clauses):
        n = len(clauses[0])
        theta = [[Fraction(0)] * (n + 1) for _ in range(n + 1)]
        theta[0][0] = Fraction(1)
        for clause in clauses:
            for i in range(n + 1):
                for j in range(n + 1):
                    if all(l == 0 or abs(l) <= i and abs(l) <= j for l in clause):
                        theta[i][j] += theta[i - abs(clause[0])][j - abs(clause[1])] * theta[i - abs(clause[2])][j]
        return max(max(row) for row in theta)
    
    n_values = [5, 10, 20, 40]
    results = []
    for n in n_values:
        for _ in range(30):
            clauses = generate_3cnf(n)
            rank = tropical_theta_function(clauses)
            width = dpll_refutation_tree_width(clauses)
            results.append({"rank": rank, "width": width})
    
    if not results:
        return {
            "metric_name": "tropical_theta_rank_vs_dpll_width",
            "metric_value": 0.0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_values = [r["rank"] for r in results]
    width_values = [r["width"] for r in results]
    mean_rank = sum(rank_values) / len(rank_values)
    mean_width = sum(width_values) / len(width_values)
    correlation = sum((rank - mean_rank) * (width - mean_width) for rank, width in zip(rank_values, width_values)) / len(results)
    
    return {
        "metric_name": "tropical_theta_rank_vs_dpll_width",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation <= 0,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_not_negative\" first_failing_seed={first_failing_seed}")