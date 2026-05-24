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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def dpll_length(cnf):
        n = len(cnf[0])
        stack = []
        assignment = [None] * (n + 1)
        
        def backtrack():
            while True:
                if not stack:
                    return len(assignment) - 1
                i, j = stack.pop()
                if assignment[j] is None:
                    assignment[j] = 1
                    for clause in cnf:
                        if all(x == 0 or (x > 0 and assignment[x] == 1) or (x < 0 and assignment[-x] == -1) for x in clause):
                            break
                    else:
                        stack.append((i, j + 1))
                        continue
                assignment[j] = -assignment[j]
                if all(x == 0 or (x > 0 and assignment[x] == 1) or (x < 0 and assignment[-x] == -1) for x in clause):
                    stack.append((i, j + 1))
                else:
                    stack.append((i, j + 1))
            return len(assignment) - 1
        
        return backtrack()
    
    def minimal_rank(cnf):
        n = len(cnf[0])
        rank = 0
        for i in range(n):
            if all(x == 0 or (x > 0 and assignment[x] == 1) or (x < 0 and assignment[-x] == -1) for x in cnf):
                rank += 1
        return rank
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    dpll_len = dpll_length(cnf)
    min_rank = minimal_rank(cnf)
    
    if dpll_len == 0:
        return {
            "metric_name": "minimal_rank_vs_dpll_length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL proof length is zero"
        }
    
    correlation = min_rank / dpll_len
    return {
        "metric_name": "minimal_rank_vs_dpll_length",
        "metric_value": correlation,
        "instances_tested": 1,
        "conjecture_holds": correlation >= 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.5) / len(results)
    
    if all(r >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r < 0.5 for r in results):
        first_failing_seed = seeds[results.index(min([r for r in results if r < 0.5]))]
        print(f"RESULT: FALSIFIED counterexample='correlation_below_0.5' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")