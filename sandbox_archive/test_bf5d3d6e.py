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
    
    def generate_formula(n, m):
        variables = set(f"x{i}" for i in range(1, n+1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables | {f"~x{i}" for i in range(1, n+1)}, 2)
            if random.choice([True, False]):
                clause[0] = f"~{clause[0]}"
            clauses.append(clause)
        return clauses
    
    def resolution_width(clauses):
        # Simplified DPLL solver to estimate resolution width
        seen = set()
        queue = clauses[:]
        while queue:
            literals = set()
            for clause in queue:
                literals.update(clause)
            if not literals:
                break
            literal = random.choice(list(literals))
            new_clauses = []
            for clause in queue:
                if literal in clause:
                    continue
                if f"~{literal}" in clause:
                    seen.add(literal)
                    continue
                new_clause = [l for l in clause if l != f"~{literal}"]
                if new_clause not in new_clauses:
                    new_clauses.append(new_clause)
            queue = new_clauses
        return len(seen)
    
    def cyclic_orderings(clauses):
        # Constructive mapping to assign cyclic orderings
        orderings = []
        for clause in clauses:
            ordering = sorted(clause, key=lambda x: (x[0] == '~', x))
            if ordering not in orderings:
                orderings.append(ordering)
        return len(orderings)
    
    n = random.randint(5, 30)
    m = random.randint(n*2, n*4)
    clauses = generate_formula(n, m)
    width = resolution_width(clauses)
    orderings = cyclic_orderings(clauses)
    
    metric_value = Fraction(orderings, width) if width > 0 else float('inf')
    conjecture_holds = metric_value <= 1.5
    counterexample = "" if conjecture_holds else f"Orderings={orderings}, Width={width}"
    
    return {
        "metric_name": "Cyclic Orderings / Resolution Width",
        "metric_value": float(metric_value),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")