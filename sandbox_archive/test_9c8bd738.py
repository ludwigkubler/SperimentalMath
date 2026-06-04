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
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if not any(clause[i] == -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def compute_lie_algebroid_order(cnf):
        m = len(cnf)
        n = len(cnf[0])
        matrix = [[0] * (n + 1) for _ in range(m)]
        for i, clause in enumerate(cnf):
            for lit in clause:
                if lit > 0:
                    matrix[i][lit - 1] += 1
                else:
                    matrix[i][-1] -= 1
        rank = 0
        for row in matrix:
            if any(row[j] != 0 for j in range(n + 1)):
                rank += 1
        return rank
    
    def resolution_width(cnf):
        queue = cnf[:]
        seen = set()
        while queue:
            clause = queue.pop(0)
            for lit in clause:
                neg_lit = -lit
                if neg_lit in seen:
                    continue
                seen.add(neg_lit)
                new_clauses = []
                for other_clause in queue:
                    if neg_lit in other_clause:
                        new_clause = [l for l in other_clause if l != neg_lit]
                        if new_clause and all(lit not in new_clause for lit in clause):
                            new_clauses.append(new_clause)
                queue.extend(new_clauses)
        return len(queue) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        lie_algebroid_order = compute_lie_algebroid_order(cnf)
        width = resolution_width(cnf)
        results.append({
            "n": n,
            "lie_algebroid_order": lie_algebroid_order,
            "width": width
        })
    
    if not results:
        return {
            "metric_name": "lie_algebroid_order_over_width",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    lie_algebroid_orders = [r["lie_algebroid_order"] for r in results]
    widths = [r["width"] for r in results]
    
    if any(w == 0 for w in widths):
        return {
            "metric_name": "lie_algebroid_order_over_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": "width_zero"
        }
    
    ratio = [lie_algebroid_orders[i] / widths[i] for i in range(len(lie_algebroid_orders))]
    
    if any(r > 2 for r in ratio):
        return {
            "metric_name": "lie_algebroid_order_over_width",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(r["n"] for r in results),
            "conjecture_holds": False,
            "counterexample": f"ratio_exceeds_2 at n={results[ratio.index(max(ratio))]['n']}"
        }
    
    return {
        "metric_name": "lie_algebroid_order_over_width",
        "metric_value": sum(ratio) / len(ratio),
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "ratio_exceeds_2"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")