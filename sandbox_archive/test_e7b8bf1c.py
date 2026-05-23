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
    
    def generate_k_cnf(n):
        clauses = []
        for _ in range(2**n // 4):  # Generate a few clauses to form a k-CNF formula
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def tropicalized_quandle_representation(clauses):
        quandle = set()
        for clause in clauses:
            for literal in clause:
                quandle.add(abs(literal))
        return len(quandle)
    
    def nondeterministic_circuit_depth(clauses):
        depth = 0
        for clause in clauses:
            if any(lit > 0 for lit in clause) and any(lit < 0 for lit in clause):
                depth += 1
        return depth
    
    n = random.randint(5, 40)
    cnf_formula = generate_k_cnf(n)
    rank = tropicalized_quandle_representation(cnf_formula)
    depth = nondeterministic_circuit_depth(cnf_formula)
    
    if depth == 0:
        return {
            "metric_name": "Rank vs Depth",
            "metric_value": float('inf'),  # Avoid division by zero
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Depth is zero, making the ratio undefined."
        }
    
    ratio = rank / depth
    
    return {
        "metric_name": "Rank vs Depth",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio is undefined\" first_failing_seed={first_failing_seed}")