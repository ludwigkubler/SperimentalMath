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
        for _ in range(n * (n - 1)):
            literals = [random.randint(1, n), random.randint(1, n)]
            if random.choice([True, False]):
                literals[0] *= -1
            if random.choice([True, False]):
                literals[1] *= -1
            cnf.append(literals)
        return cnf
    
    def resolution_width(cnf):
        # Simplified DPLL algorithm to estimate width
        stack = []
        for clause in cnf:
            stack.append(clause)
        width = 0
        while stack:
            clause = stack.pop()
            if not clause:
                return float('inf')
            literal = random.choice(clause)
            new_clauses = []
            for c in cnf:
                if literal in c:
                    continue
                if -literal in c:
                    new_clauses.append([l for l in c if l != -literal])
                else:
                    new_clauses.append(c + [l for l in clause if l != literal])
            stack.extend(new_clauses)
            width = max(width, len(stack))
        return width
    
    def local_cohomology_rank(n):
        # Simplified mapping to compute a rank
        rank = 0
        for i in range(1, n + 1):
            if random.choice([True, False]):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    lchrank = local_cohomology_rank(n)
    width = resolution_width(cnf)
    
    if width == float('inf'):
        return {
            "metric_name": "lchrank/width_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Resolution width is infinite"
        }
    
    ratio = Fraction(lchrank, width)
    return {
        "metric_name": "lchrank/width_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio >= Fraction(1, 2),
        "counterexample": f"Ratio {ratio} < 0.5" if ratio < Fraction(1, 2) else ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio {result['metric_value']} < 0.5\" first_failing_seed={first_failing_seed}")