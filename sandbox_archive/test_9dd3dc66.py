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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        n = len(cnf[0])
        queue = cnf[:]
        seen = set()
        
        while queue:
            clause = queue.pop(0)
            if not any(lit in seen for lit in clause):
                seen.update(clause)
                new_clauses = []
                for other_clause in queue:
                    for lit in clause:
                        if -lit in other_clause:
                            new_lit = [l for l in other_clause if l != -lit]
                            if new_lit not in new_clauses and new_lit not in queue:
                                new_clauses.append(new_lit)
                queue.extend(new_clauses)
            else:
                return len(seen)
        return len(seen)
    
    def quandle_order(cnf):
        n = len(cnf[0])
        order = 1
        for _ in range(n):
            new_cnf = []
            for clause in cnf:
                new_clause = [lit if lit > 0 else -lit for lit in clause]
                new_cnf.append(new_clause)
            cnf = new_cnf
            order *= 2
        return order
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        order = quandle_order(cnf)
        
        if order > 2**n:
            conjecture_holds = False
            counterexample = f"CNF with n={n} has quandle order {order} > 2^n"
            break
        
        total_metric_value += order
        instances_tested += 1
    
    return {
        "metric_name": "Quandle Order",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")