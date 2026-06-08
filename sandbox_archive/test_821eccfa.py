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
    
    def generate_braided_group(n):
        # Placeholder for generating a braided group
        return [random.randint(1, n) for _ in range(n)]
    
    def construct_cnf_formula(group):
        # Placeholder for constructing a CNF formula from a braided group
        cnf = []
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                if group[i] != group[j]:
                    cnf.append([i + 1, -j - 1])
        return cnf
    
    def compute_minimal_rank(group):
        # Placeholder for computing the minimal rank of a braided group
        n = len(group)
        rank = 0
        while True:
            found = False
            for i in range(n):
                if group[i] not in group[:i]:
                    rank += 1
                    break
            else:
                return rank
    
    def compute_resolution_proof_width(cnf):
        # Placeholder for computing the resolution proof width of a CNF formula
        n = len(cnf)
        width = 0
        while True:
            found = False
            for clause in cnf:
                if len(clause) > width:
                    width = len(clause)
                    break
            else:
                return width
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        group = generate_braided_group(n)
        cnf = construct_cnf_formula(group)
        
        rank = compute_minimal_rank(group)
        proof_width = compute_resolution_proof_width(cnf)
        
        results.append({
            "metric_name": "correlation_coefficient",
            "metric_value": rank / proof_width if proof_width > 0 else None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": ""
        })
    
    correlation_coefficient = sum(r["metric_value"] for r in results) / len(results)
    conjecture_holds = correlation_coefficient >= 0.95 and all(abs(r["metric_value"] - proof_width) <= 20 for r in results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "insufficient_instances"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(abs(r["metric_value"] - proof_width) > 20 for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if abs(r["metric_value"] - proof_width) > 20)
        print(f"RESULT: FALSIFIED counterexample='insufficient_instances' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_instances")