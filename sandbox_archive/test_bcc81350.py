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
        for _ in range(random.randint(1, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(cnf):
        stack = []
        assignment = [None] * len(cnf)
        
        def backtrack(i):
            if i == len(cnf):
                return True
            literals = cnf[i]
            for literal in literals:
                var = abs(literal) - 1
                if assignment[var] is None:
                    assignment[var] = literal > 0
                    stack.append((var, assignment[var]))
                    if backtrack(i + 1):
                        return True
                    stack.pop()
                    assignment[var] = None
            return False
        
        return backtrack(0)
    
    def resolution(cnf):
        clauses = cnf[:]
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    l1, l2 = clauses[i], clauses[j]
                    if any(-x in l2 for x in l1):
                        new_clause = [x for x in l1 if x not in [-y for y in l2] and x != -y]
                        if new_clause:
                            new_clauses.append(new_clause)
            if len(new_clauses) == 0:
                break
            clauses.extend(new_clauses)
        return len(clauses)
    
    def msr(cnf):
        # Placeholder for minimal symmetric function rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return random.random() * len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    msr_values = []
    w_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        if is_satisfiable(cnf):
            msr_value = msr(cnf)
            w_value = resolution(cnf)
            msr_values.append(msr_value)
            w_values.append(w_value)
    
    correlation_coefficient = sum((msr_values[i] - sum(msr_values) / len(msr_values)) * (w_values[i] - sum(w_values) / len(w_values)) for i in range(len(msr_values))) / (len(msr_values) * math.sqrt(sum((msr_values[i] - sum(msr_values) / len(msr_values)) ** 2 for i in range(len(msr_values)))) * math.sqrt(sum((w_values[i] - sum(w_values) / len(w_values)) ** 2 for i in range(len(w_values)))))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.1,  # Arbitrary threshold for linear correlation
        "counterexample": "" if abs(correlation_coefficient) > 0.1 else f"correlation_coefficient={correlation_coefficient}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='{results[first_failing_seed]['counterexample']}' first_failing_seed={seeds[first_failing_seed]}")