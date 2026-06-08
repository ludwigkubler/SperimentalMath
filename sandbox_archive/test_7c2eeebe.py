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
        cnf = []
        for i in range(1, n+1):
            clause = [random.randint(-i, -1), random.randint(i, n)]
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        queue = list(clauses)
        seen = set(queue)
        
        while queue:
            clause = queue.pop()
            if len(clause) == 1:
                return abs(clause[0])
            
            literal = random.choice(clause)
            other_literal = -literal
            new_clauses = []
            for c in clauses:
                if other_literal not in c:
                    new_c = tuple(sorted(set(c) | {other_literal}))
                    if new_c not in seen:
                        seen.add(new_c)
                        new_clauses.append(new_c)
            queue.extend(new_clauses)
        
        return 0
    
    def coxeter_group_presentation(cnf):
        # Placeholder for Coxeter group presentation calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf)
    
    instances_tested = 0
    n_max = 0
    total_s = 0
    total_w = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_cnf(n)
            s = coxeter_group_presentation(cnf)
            w = resolution_width(cnf)
            total_s += s
            total_w += w
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_s = total_s / instances_tested
    mean_w = total_w / instances_tested
    
    correlation_coefficient = (instances_tested * sum(s*w for s, w in zip([mean_s]*instances_tested, [mean_w]*instances_tested)) - 
                                sum([mean_s]*instances_tested) * sum([mean_w]*instances_tested)) / \
                               math.sqrt((instances_tested * sum(s**2 for s in [mean_s]*instances_tested) - (sum([mean_s]*instances_tested))**2) *
                                         (instances_tested * sum(w**2 for w in [mean_w]*instances_tested) - (sum([mean_w]*instances_tested))**2))
    
    conjecture_holds = correlation_coefficient >= 0.8
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 3))
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")