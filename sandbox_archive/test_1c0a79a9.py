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
        for _ in range(2**n // 3):  # Ensure not all assignments are satisfying
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.random() < 0.5:
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_satisfying(cnf, assignment):
        return any(all(assignment[abs(l)-1] * l > 0 for l in clause) for clause in cnf)
    
    def renyi_divergence(p, alpha):
        if p == 0:
            return float('inf')
        return (p ** alpha - 1) / (alpha - 1)
    
    def resolution_width(cnf):
        clauses = [set(clause) for clause in cnf]
        queue = set()
        learned = set()
        
        for clause in clauses:
            if len(clause) == 1:
                queue.add(clause)
            else:
                learned.add(frozenset(clause))
        
        width = 0
        while queue:
            new_queue = set()
            for clause1 in queue:
                for clause2 in queue:
                    if not clause1.isdisjoint(clause2):
                        diff = clause1 ^ clause2
                        if len(diff) == 1:
                            new_queue.add(frozenset(diff))
                        else:
                            learned.add(frozenset(diff))
            width += len(queue)
            queue = new_queue
        
        return width
    
    n_max = 0
    total_metric_value = 0
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > 40:
            break
        
        cnf = generate_cnf(n)
        n_max = max(n_max, len(cnf))
        
        satisfying_assignments = sum(is_satisfying(cnf, assignment) for assignment in product([-1, 1], repeat=n))
        total_probability = Fraction(satisfying_assignments, 2**n)
        metric_value = renyi_divergence(total_probability, 1.5)  # Using alpha=1.5 as a test case
        
        if metric_value == float('inf'):
            conjecture_holds = False
            counterexample = "Rényi divergence is infinite for some assignment"
            break
        
        resolution_wid = resolution_width(cnf)
        ratio = Fraction(metric_value, resolution_wid)
        
        total_metric_value += metric_value
        instances_tested += 1
        
        if ratio > c_alpha:
            conjecture_holds = False
            counterexample = f"Ratio {ratio} exceeds bound for n={n}"
            break
    
    return {
        "metric_name": "Rényi Divergence",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    from itertools import product
    
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={seeds[0]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence to support or refute the conjecture")