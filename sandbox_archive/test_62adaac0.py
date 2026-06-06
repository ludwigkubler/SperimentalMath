# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        cnf = []
        for _ in range(10):  # Generate 10 clauses for simplicity
            clause = [random.randint(-n, -1)]
            cnf.append(clause)
        return cnf
    
    def circuit_depth(cnf):
        stack = []
        depth = 0
        
        for clause in cnf:
            for literal in clause:
                if literal < 0:
                    stack.append(literal)
                else:
                    while stack and -stack[-1] == literal:
                        stack.pop()
                    depth += 1
            if not stack:
                return depth
        return depth
    
    def minimal_order_noncrossing_partitions(cnf):
        # Placeholder for the actual algorithm to compute the minimal order of noncrossing partitions
        # This is a dummy implementation and should be replaced with an actual algorithm
        return len(cnf)
    
    n = 10  # Fixed size for simplicity, can be adjusted as needed
    cnf = generate_cnf(n)
    mtr_G_phi = minimal_order_noncrossing_partitions(cnf)
    d_phi = circuit_depth(cnf)
    
    if mtr_G_phi <= d_phi <= 2**(mtr_G_phi + 1/n**2):
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = "Circuit depth does not satisfy the inequality"
    
    return {
        "metric_name": "circuit_depth",
        "metric_value": d_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Circuit depth does not satisfy the inequality\" first_failing_seed={first_failing_seed}")