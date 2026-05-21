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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            literals = [random.choice([i, -i]) for i in range(1, n + 1)]
            random.shuffle(literals)
            clause = tuple(sorted(literals))
            if clause not in clauses:
                clauses.append(clause)
        return clauses

    def is_satisfied(clause, assignment):
        return any(assignment[abs(lit)] == (lit > 0) for lit in clause)

    def generate_algebra(clauses, n):
        algebra = set()
        variables = [f'x{i}' for i in range(1, n + 1)]
        relations = [(i, j) for i in range(n) for j in range(i + 1, n)]
        
        def add_relation(x, y):
            if (x, y) in relations:
                algebra.add((x, y))
                algebra.add((y, x))
        
        for clause in clauses:
            for lit1, lit2 in itertools.combinations(clause, 2):
                var1 = variables[abs(lit1) - 1]
                var2 = variables[abs(lit2) - 1]
                add_relation(var1, var2)
        
        return algebra

    def dimension(algebra, k):
        if not algebra:
            return 0
        basis = set()
        for rel in algebra:
            if all(rel[i] not in basis for i in range(2)):
                basis.add(rel[0])
                basis.add(rel[1])
        return len(basis)

    n = 40
    clauses = generate_3cnf(n)
    
    algebra = generate_algebra(clauses, n)
    growth_rate = [dimension(algebra, k) for k in range(1, 11)]
    
    tseitin_width = math.log2(n)
    
    metric_name = "growth_rate"
    metric_value = sum(growth_rate) / len(growth_rate)
    instances_tested = len(growth_rate)
    conjecture_holds = all(x >= 2**(k/2) for k, x in enumerate(growth_rate))
    counterexample = "" if conjecture_holds else "growth_rate_mismatch"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"growth_rate_mismatch\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_conjecture_support")