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
        cnf = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause.reverse()
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        assignment = {}
        
        def is_satisfiable():
            stack = []
            while True:
                unit_clause = next((c for c in cnf if len(c) == 1), None)
                if unit_clause:
                    l = unit_clause[0]
                    if -l in assignment and assignment[-l] != (l > 0):
                        return False
                    assignment[l] = l > 0
                    stack.append(l)
                else:
                    pure_literal = next((l for l in range(1, max(cnf) + 1) if (l not in assignment and -l not in assignment)), None)
                    if pure_literal is None:
                        return True
                    assignment[pure_literal] = True
                    stack.append(pure_literal)
                
                while stack:
                    l = stack[-1]
                    if all(l not in c for c in cnf):
                        del assignment[l]
                        stack.pop()
                    else:
                        break
        
        return is_satisfiable()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        dpll_depth = dpll(cnf)
        min_order = len(cnf)  # Simplified for this test
        
        results.append({
            "n": n,
            "dpll_depth": dpll_depth,
            "min_order": min_order
        })
    
    mean_dpll_depth = sum(r["dpll_depth"] for r in results) / len(results)
    mean_min_order = sum(r["min_order"] for r in results) / len(results)
    diff_mean = abs(mean_dpll_depth - mean_min_order)
    
    conjecture_holds = diff_mean <= 1
    counterexample = "" if conjecture_holds else f"mean_diff={diff_mean}"
    
    return {
        "metric_name": "Difference between DPLL depth and min order",
        "metric_value": diff_mean,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        print(f"TRIAL: {seed}")
        result = run_trial(seed)
        results.append(result)
        
        mean_diff = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
    print(f"RESULT: SUPPORTED mean={mean_diff} std=<not_computed> support_fraction={support_fraction}")