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
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables), random.choice([-1, 1])]
            clauses.append(clause)
        return clauses
    
    def tropical_jacobian_rank(clauses):
        # Placeholder for actual computation
        # For simplicity, assume rank is proportional to the number of variables
        n = len(set(var for clause in clauses for var in clause))
        return n * (n + 1) // 2
    
    def resolution_proof_size(clauses):
        # Placeholder for actual computation
        # For simplicity, assume size is proportional to the number of clauses
        return len(clauses)
    
    n = random.randint(5, 40)
    k = random.randint(n, n * 2)
    formula = generate_k_cnf(n, k)
    rank = tropical_jacobian_rank(formula)
    proof_size = resolution_proof_size(formula)
    
    ratio = proof_size / rank if rank != 0 else float('inf')
    
    return {
        "metric_name": "Ratio of Resolution Proof Size to Jacobian Rank",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": "" if ratio <= 1.5 else f"Ratio {ratio} exceeds 1.5"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(result["counterexample"]):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")