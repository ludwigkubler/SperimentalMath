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
    
    def generate_k_cnf(k, n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(k)]
            while len(set(abs(x) for x in clause)) < k:
                clause[random.randint(0, k-1)] *= -1
            clauses.append(clause)
        return clauses
    
    def tropicalize_affine_scheme(cnf):
        rank = 0
        for clause in cnf:
            rank += max(abs(x) for x in clause)
        return rank
    
    def resolution_length(cnf):
        stack = [cnf]
        length = 0
        while stack:
            clause = stack.pop()
            if not any(clause[i] == -clause[j] for i, j in itertools.combinations(range(len(clause)), 2)):
                return float('inf')
            new_clause = []
            for c1 in clause:
                for c2 in stack:
                    if abs(c1) != abs(c2):
                        new_clause.append(c1 + c2)
            stack.extend(new_clause)
            length += 1
        return length
    
    n = random.randint(5, 40)
    k = 3
    cnf = generate_k_cnf(k, n)
    rank = tropicalize_affine_scheme(cnf)
    proof_length = resolution_length(cnf)
    
    if proof_length == float('inf'):
        return {
            "metric_name": "proof_length_to_rank_ratio",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "resolution_length_infinite"
        }
    
    ratio = proof_length / rank**2
    return {
        "metric_name": "proof_length_to_rank_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 2 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] > 2)
        print(f"RESULT: FALSIFIED counterexample=\"proof_length_too_long\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")