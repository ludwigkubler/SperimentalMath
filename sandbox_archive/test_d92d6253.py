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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def p_adic_representation(clauses):
        # Simplified representation using a dictionary to count occurrences
        rep = {}
        for clause in clauses:
            for lit in clause:
                if lit not in rep:
                    rep[lit] = 0
                rep[lit] += 1
        return rep
    
    def rank_of_representation(rep):
        # Count unique keys in the representation dictionary
        return len(rep)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(3, 6)  # Ensure k ≥ 3
        formula = generate_k_cnf(n, k)
        rep = p_adic_representation(formula)
        rank = rank_of_representation(rep)
        
        expected_rank = math.sqrt(n) * (k ** 0.25)
        within_margin = abs(rank - expected_rank) <= 0.2 * expected_rank
        
        results.append({
            "n": n,
            "k": k,
            "formula": formula,
            "rep": rep,
            "rank": rank,
            "expected_rank": expected_rank,
            "within_margin": within_margin
        })
    
    metric_value = sum(r["within_margin"] for r in results) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(r["within_margin"] for r in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Average Rank",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")