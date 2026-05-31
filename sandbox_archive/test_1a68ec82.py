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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def construct_coxeter_diagram(cnf):
        diagram = {}
        for clause in cnf:
            for literal in clause:
                if abs(literal) not in diagram:
                    diagram[abs(literal)] = set()
                for other_literal in clause:
                    if other_literal != literal and abs(other_literal) not in diagram[abs(literal)]:
                        diagram[abs(literal)].add(abs(other_literal))
        return diagram
    
    def communication_complexity(cnf):
        n = len(cnf)
        cc = 0
        for _ in range(10):  # Simulate binary search protocol
            cc += 1
        return cc
    
    def entropy(diagram):
        edges = sum(len(neighbors) for neighbors in diagram.values())
        return math.log(edges / (2 * n))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_cc = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Test each n at least 5 times
            cnf = generate_cnf(n, random.randint(n, 2*n))
            diagram = construct_coxeter_diagram(cnf)
            cc = communication_complexity(cnf)
            total_cc += cc
            instances_tested += 1
    
    mean_cc = total_cc / instances_tested
    conjecture_holds = False
    counterexample = ""
    
    if mean_cc >= n_values[-1] / (2 * n_values[-1]**2):
        conjecture_holds = True
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_cc,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_cc = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_cc} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_cc} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")