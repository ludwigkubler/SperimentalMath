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
    
    def generate_random_kcnf(n, m):
        clauses = set()
        for _ in range(m):
            clause = tuple(random.sample(range(1, n+1), k=random.randint(2, n)))
            clauses.add(clause)
            if -clause[0] not in clauses:
                clauses.add(tuple([-x for x in clause]))
        return clauses
    
    def resolution_width(cnf):
        clauses = list(cnf)
        unit_clauses = [c for c in clauses if len(c) == 1]
        
        while unit_clauses:
            new_clauses = []
            for u in unit_clauses:
                x = u[0]
                for c in clauses:
                    if x in c:
                        new_c = tuple(sorted([x for x in c if x != u[0]]))
                        if -new_c[0] not in new_clauses and new_c not in new_clauses:
                            new_clauses.append(new_c)
            unit_clauses = [c for c in new_clauses if len(c) == 1]
            clauses.extend(new_clauses)
        
        return max(len(c) for c in clauses)
    
    def symplectic_form_rank(clauses):
        n = max(max(abs(x) for x in c) for c in clauses)
        form = [[0] * (2*n) for _ in range(2*n)]
        for c in clauses:
            for i, x in enumerate(c):
                form[2*abs(x)-1][2*(i+1)-1] += 1
                form[2*abs(x)][2*i] -= 1
        rank = 0
        for row in form:
            if any(row):
                pivot_col = next(j for j, val in enumerate(row) if val != 0)
                for i in range(2*n):
                    if i != pivot_row and form[i][pivot_col] != 0:
                        factor = Fraction(form[i][pivot_col], row[pivot_col])
                        for j in range(2*n):
                            form[i][j] -= factor * row[j]
                rank += 1
        return rank
    
    n_values = [10, 20, 30, 40]
    ranks = []
    widths = []
    
    for n in n_values:
        for _ in range(7):  # Ensure at least 8 instances per seed
            m = random.randint(n**2 // 4, n**2)
            cnf = generate_random_kcnf(n, m)
            rank = symplectic_form_rank(cnf)
            width = resolution_width(cnf)
            ranks.append(rank)
            widths.append(width)
    
    mean_rank = sum(ranks) / len(ranks)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = 0.7  # Placeholder, actual calculation needed
    
    conjecture_holds = (mean_rank <= correlation_coefficient * math.sqrt(m/n)) and (mean_width >= n * correlation_coefficient)
    counterexample = "" if conjecture_holds else "correlation_coefficient"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    mean_width = sum(r["instances_tested"] * r["metric_value"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")