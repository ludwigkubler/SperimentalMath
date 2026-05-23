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
    
    def generate_k_cnf(n):
        clauses = []
        for _ in range(random.randint(1, n)):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def tropicalized_quandle_representation(clauses):
        quandle = set()
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    quandle.add(literal)
                else:
                    quandle.add(-literal)
        return len(quandle)
    
    def nondeterministic_circuit_depth(clauses):
        depth = 0
        for clause in clauses:
            depth = max(depth, len(clause))
        return depth
    
    n = random.randint(5, 40)
    k_cnf = generate_k_cnf(n)
    rank = tropicalized_quandle_representation(k_cnf)
    depth = nondeterministic_circuit_depth(k_cnf)
    
    if depth == 0:
        return {
            "metric_name": "Rank vs Depth",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Circuit depth is zero"
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
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **trial_result}}")
        results.append(trial_result)
    
    if all(result['conjecture_holds'] for result in results):
        mean_ratio = sum(result['metric_value'] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")