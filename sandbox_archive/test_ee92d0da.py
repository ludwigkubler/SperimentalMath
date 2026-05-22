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
        clauses = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def quantifier_depth(cnf):
        depth = 0
        for clause in cnf:
            if any(abs(lit) > len(cnf) for lit in clause):
                depth += 1
        return depth
    
    def construct_scheme(cnf):
        n = len(cnf)
        points = [(i, j) for i in range(n) for j in range(n)]
        lines = []
        for clause in cnf:
            x1, y1 = random.choice(points)
            x2, y2 = random.choice(points)
            while (x1 == x2 and y1 == y2):
                x2, y2 = random.choice(points)
            lines.append(((x1, y1), (x2, y2)))
        return points, lines
    
    def minimal_rank(points, lines):
        rank = 0
        for point in points:
            if any(point[0] == line[0][0] and point[1] == line[0][1] or 
                   point[0] == line[1][0] and point[1] == line[1][1] for line in lines):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    k = random.randint(1, n)
    cnf = generate_k_cnf(n, k)
    d = quantifier_depth(cnf)
    
    if d == 0:
        return {
            "metric_name": "Minimal Rank",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Quantifier depth is zero"
        }
    
    points, lines = construct_scheme(cnf)
    rank = minimal_rank(points, lines)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= d * d,  # Polynomial bound C*d^2
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(10000, 99999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")