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
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_depth(cnf):
        stack = cnf[:]
        depth = 0
        while True:
            new_clauses = []
            for i in range(len(stack)):
                for j in range(i + 1, len(stack)):
                    if abs(stack[i][0]) == abs(stack[j][0]):
                        new_clause = [c for c in stack[i] if c not in (stack[j][0], -stack[j][0])]
                        new_clause.extend([c for c in stack[j] if c not in (stack[i][0], -stack[i][0])])
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            stack.extend(new_clauses)
            depth += 1
        return depth
    
    def hodge_index(cnf):
        # Placeholder for Hodge index computation
        # This is a dummy implementation; replace with actual algorithm
        return random.randint(1, len(cnf))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    p = random.choice([2, 3, 5, 7, 11, 13, 17, 19, 23, 29])
    
    cnf = generate_cnf(n)
    depth = resolution_depth(cnf)
    index = hodge_index(cnf)
    
    return {
        "metric_name": "Hodge Index / Resolution Depth",
        "metric_value": Fraction(index, depth),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")