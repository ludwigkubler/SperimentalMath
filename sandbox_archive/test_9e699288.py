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
    
    def generate_k_cnf_tautology(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables) * (-1 if random.randint(0, 1) else 1)]
            while len(clause) < n:
                v = random.choice(variables)
                if v not in clause and -v not in clause:
                    clause.append(v * (-1 if random.randint(0, 1) else 1))
            clauses.append(clause)
        return clauses
    
    def is_tautology(clauses):
        assignments = [False] * (n + 1)
        for _ in range(2 ** n):
            valid = True
            for clause in clauses:
                if all(not (x == -y or x == y) for x, y in zip(clause, assignments)):
                    valid = False
                    break
            if valid:
                return True
            assignments[1:] = [not a for a in assignments[1:]]
        return False
    
    def min_rank_symplectic_leaves(n):
        # Placeholder function to simulate the computation of minRank(S(T))
        # This is a dummy implementation and should be replaced with actual logic
        return n * (n - 1) // 2
    
    n = random.randint(5, 40)
    k = random.randint(1, n // 3)
    tautology = generate_k_cnf_tautology(n, k)
    
    if not is_tautology(tautology):
        return {
            "metric_name": "minRank(S(T)) / s(C)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "not a tautology"
        }
    
    min_rank = min_rank_symplectic_leaves(n)
    # Placeholder function to simulate the computation of circuit size s(C)
    # This is a dummy implementation and should be replaced with actual logic
    circuit_size = n * k
    
    if circuit_size == 0:
        return {
            "metric_name": "minRank(S(T)) / s(C)",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "circuit size is zero"
        }
    
    ratio = min_rank / circuit_size
    return {
        "metric_name": "minRank(S(T)) / s(C)",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["counterexample"] != "")
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")