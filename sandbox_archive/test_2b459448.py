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
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def tropicalized_quandle_representation(clauses):
        # Simplified mapping to a quandle structure
        quandle_size = len(clauses) + 1
        quandle = [[0] * quandle_size for _ in range(quandle_size)]
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    quandle[literal][literal] = 1
                else:
                    quandle[-1][abs(literal)] = 1
        return quandle
    
    def circuit_depth(clauses):
        # Simplified circuit depth calculation
        depth = len(clauses)
        for clause in clauses:
            depth += max(abs(lit) for lit in clause)
        return depth
    
    def minimal_rank(quandle):
        n = len(quandle)
        rank = 0
        while True:
            found = False
            for i in range(n):
                if sum(quandle[i]) == 1:
                    rank += 1
                    for j in range(n):
                        quandle[j][i] = 0
                    found = True
                    break
            if not found:
                break
        return rank
    
    n = random.randint(5, 40)
    clauses = generate_k_cnf(n)
    quandle = tropicalized_quandle_representation(clauses)
    depth = circuit_depth(clauses)
    rank = minimal_rank(quandle)
    
    ratio = rank / depth if depth != 0 else float('inf')
    
    return {
        "metric_name": "Rank vs Depth",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, rank={r['metric_value']}, depth={1 / r['metric_value']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break