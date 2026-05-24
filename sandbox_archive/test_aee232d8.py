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
    
    def generate_k_sat_instance(n, m):
        clauses = set()
        for _ in range(m):
            clause = []
            while len(clause) == 0 or len(set(abs(lit) for lit in clause)) != n:
                literals = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
                if all(lit not in clause and -lit not in clause for lit in literals):
                    clause.extend(literals)
            clauses.add(tuple(sorted(clause)))
        return clauses
    
    def p_adic_order(differential):
        order = 0
        while differential % 2 == 0:
            differential //= 2
            order += 1
        return order
    
    def resolution_depth(clauses):
        n = len(clauses)
        if n == 0:
            return 0
        
        stack = list(clauses)
        depth = 0
        
        while stack:
            clause = stack.pop()
            if all(lit in stack for lit in clause):
                return depth
            new_clause = set()
            for c1 in stack:
                for c2 in clauses:
                    if len(c1.intersection(c2)) == 1:
                        new_clause.update([l for l in c1 if l not in c2] + [l for l in c2 if l not in c1])
            stack.append(tuple(sorted(new_clause)))
            depth += 1
        
        return float('inf')
    
    n = random.randint(5, 40)
    m = min(n**2, random.randint(5, 40))
    instance = generate_k_sat_instance(n, m)
    
    differential = sum(random.choice([-1, 1]) * (i + 1) for i in range(n))
    p_order = p_adic_order(differential)
    res_depth = resolution_depth(instance)
    
    metric_name = "p-Adic Order vs Resolution Depth"
    metric_value = p_order
    instances_tested = 1
    conjecture_holds = (p_order <= math.log(n) + math.log(m)) and (res_depth >= n**2)
    counterexample = "" if conjecture_holds else f"p-order={p_order}, res-depth={res_depth}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"p-order exceeded log(n) + log(m)\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")