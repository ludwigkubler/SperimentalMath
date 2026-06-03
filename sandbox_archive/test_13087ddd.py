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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if random.choice([True, False]):
                clause[0], clause[1] = clause[1], clause[0]
            cnf.append(clause)
        return cnf
    
    def resolve(cnf, literals):
        new_literals = set(literals)
        while True:
            new_cnf = []
            for clause in cnf:
                if not any(abs(lit) in new_literals for lit in clause):
                    continue
                new_clause = [lit for lit in clause if abs(lit) not in new_literals]
                if len(new_clause) == 0:
                    return True, new_literals
                elif len(new_clause) == 1:
                    new_literals.add(-new_clause[0])
                else:
                    new_cnf.append(new_clause)
            cnf = new_cnf
        return False, new_literals
    
    def count_distinct_roots(p):
        roots = set()
        for i in range(-100, 101):
            if p(i) == 0:
                roots.add(i)
        return len(roots)
    
    def polynomial(cnf):
        n = max(abs(lit) for lit in sum(cnf, []))
        p = [Fraction(0)] * (n + 1)
        for clause in cnf:
            term = Fraction(1)
            for lit in clause:
                if lit > 0:
                    term *= (x - lit)
                else:
                    term *= (x + abs(lit))
            p += term
        return p
    
    def degree(p):
        return len(p) - 1
    
    def leading_coefficient(p):
        return p[degree(p)]
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_roots = 0
    total_widths = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n))
            p = polynomial(cnf)
            roots_count = count_distinct_roots(p)
            width, _ = resolve(cnf, set())
            total_roots += roots_count
            total_widths += width
            instances_tested += 1
    
    mean_roots = Fraction(total_roots, instances_tested)
    mean_width = Fraction(total_widths, instances_tested)
    
    if mean_roots <= 1.5 * mean_width:
        conjecture_holds = True
        counterexample = ""
    else:
        conjecture_holds = False
        counterexample = f"mean_roots={mean_roots}, mean_width={mean_width}"
    
    return {
        "metric_name": "roots_to_width_ratio",
        "metric_value": float(mean_roots / mean_width),
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")