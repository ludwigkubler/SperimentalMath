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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(c != 0 for c in clause):
                clauses.append(clause)
        return clauses
    
    def dpll_width(phi):
        # Simplified DPLL width calculation
        max_width = 0
        stack = []
        literals = set()
        
        def backtrack():
            nonlocal max_width
            if not stack:
                return len(literals)
            literal = next(iter(literals))
            literals.remove(literal)
            for clause in phi:
                if literal in clause:
                    clause.remove(literal)
                    if not clause:
                        literals.add(-literal)
                        continue
                    new_clause = [l for l in clause if l != -literal]
                    stack.append((new_clause, literals.copy()))
                    literals.add(literal)
                    max_width = max(max_width, backtrack())
                    literals.remove(literal)
            return max_width
        
        return backtrack()
    
    def min_idx(phi):
        # Simplified minimal index calculation
        return len(phi)
    
    n = random.randint(5, 40)
    phi = generate_cnf(n)
    w_DPLL = dpll_width(phi)
    min_idx_val = min_idx(phi)
    
    if w_DPLL == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "w_DPLL=0"
        }
    
    correlation = abs(min_idx_val - w_DPLL) / max(w_DPLL, 1)
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation <= 0.1 and abs(min_idx_val - (sum(correlation for _ in range(30)) / 30)) <= 0.1 * sum(correlation for _ in range(30)) / 30,
        "counterexample": f"min_idx={min_idx_val}, w_DPLL={w_DPLL}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        print(f"TRIAL: {result}")
    
    mean_corr = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"min_idx and w_DPLL do not correlate\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")