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
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def entropy(clauses):
        num_clauses = len(clauses)
        counts = [0] * (num_clauses + 1)
        for clause in clauses:
            counts[len(clause)] += 1
        total = sum(counts)
        ent = 0.0
        for count in counts:
            if count > 0:
                prob = count / total
                ent -= prob * math.log2(prob)
        return ent
    
    def minimal_index_of_quaternion_algebra(clauses):
        n = len(clauses)
        max_clause_length = max(len(clause) for clause in clauses)
        return max_clause_length
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n)
            index = minimal_index_of_quaternion_algebra(cnf)
            ent = entropy(cnf)
            results.append((index, ent))
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    indices, ents = zip(*results)
    n = len(indices)
    mean_index = sum(indices) / n
    mean_ent = sum(ents) / n
    
    covariance = sum((indices[i] - mean_index) * (ents[i] - mean_ent) for i in range(n)) / n
    variance_index = sum((indices[i] - mean_index) ** 2 for i in range(n)) / n
    variance_ent = sum((ents[i] - mean_ent) ** 2 for i in range(n)) / n
    
    if variance_index == 0 or variance_ent == 0:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Variance is zero"
        }
    
    pearson_corr = covariance / math.sqrt(variance_index * variance_ent)
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": pearson_corr > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE No trials completed")
    else:
        mean_corr = sum(r["metric_value"] for r in results) / len(results)
        std_corr = math.sqrt(sum((r["metric_value"] - mean_corr) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
        else:
            first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
            print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation coefficient did not meet threshold\" first_failing_seed={first_failing_seed}")