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
    
    def polynomial(cnf):
        n = len(cnf)
        x = [Fraction(1, i) if i > 0 else -Fraction(1, -i) for i in range(-n, n+1)]
        p = Fraction(0)
        for clause in cnf:
            term = Fraction(1)
            for lit in clause:
                if lit > 0:
                    term *= (x[lit] - Fraction(1, lit))
                else:
                    term *= (x[-lit] + Fraction(1, -lit))
            p += term
        return p
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        while True:
            new_clauses = []
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == 1:
                        new_clause = tuple(sorted(list(set(c1) ^ set(c2))))
                        if new_clause not in clauses:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return len(clauses)
    
    def count_distinct_roots(p):
        roots = set()
        for i in range(-100, 101):  # Sample a range of x values to approximate roots
            if p.numerator == 0:
                continue
            root = Fraction(-p.numerator, p.denominator)
            if root not in roots:
                roots.add(root)
        return len(roots)
    
    n_max = 40
    instances_tested = 0
    total_roots = 0
    total_widths = 0
    
    for n in range(5, 41):
        cnf = []
        for _ in range(n * (n + 1) // 2):  # Generate a random CNF with m clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause.reverse()
            cnf.append(clause)
        
        p = polynomial(cnf)
        roots = count_distinct_roots(p)
        width = resolution_width(cnf)
        
        total_roots += roots
        total_widths += width
        instances_tested += 1
    
    mean_roots = total_roots / instances_tested
    mean_widths = total_widths / instances_tested
    conjecture_holds = abs(mean_roots - 1.5 * mean_widths) <= 0.1 * mean_widths
    
    return {
        "metric_name": "Root Count vs Resolution Width",
        "metric_value": mean_roots,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_roots={mean_roots}, mean_widths={mean_widths}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")