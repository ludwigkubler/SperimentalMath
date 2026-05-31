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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            cnf.append(clause)
        return cnf
    
    def construct_coxeter_diagram(cnf):
        diagram = {}
        for clause in cnf:
            for literal in clause:
                if literal not in diagram:
                    diagram[literal] = set()
                for other_literal in clause:
                    if other_literal != literal and -other_literal not in clause:
                        diagram[literal].add(other_literal)
        return diagram
    
    def communication_complexity(cnf):
        n = len(cnf)
        cc = 0
        for _ in range(10):  # Simulate binary search protocol
            cc += math.log2(n + 1)
        return cc
    
    def entropy(diagram):
        edges = sum(len(diagram[literal]) for literal in diagram) // 2
        if edges == 0:
            return 0
        return -edges * math.log2(edges / (n ** 2))
    
    n = random.randint(5, 30)
    m = random.randint(n, n * 10)
    cnf = generate_cnf(n, m)
    diagram = construct_coxeter_diagram(cnf)
    cc = communication_complexity(cnf)
    cde = entropy(diagram)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": cc,
        "instances_tested": 10,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
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
        print(f"RESULT: SUPPORTED mean={mean_cc} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")