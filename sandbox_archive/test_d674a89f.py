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
        p = sum([sum([x[i] ** abs(lit) for lit in clause]) for clause in cnf])
        return p
    
    def resolution_width(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        resolved = set()
        while True:
            new_resolved = set()
            for clause1, clause2 in itertools.combinations(resolved, 2):
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = [lit for lit in clause1 + clause2 if lit not in (set(clause1) & set(clause2))]
                    new_resolved.add(tuple(sorted(new_clause)))
            if new_resolved.issubset(resolved):
                break
            resolved.update(new_resolved)
        return len(resolved)
    
    def count_distinct_roots(p):
        roots = set()
        for i in range(-100, 101):
            val = p.subs(x[i])
            if abs(val) < 1e-6:
                roots.add(i)
        return len(roots)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = [[random.choice([-i, i]) for _ in range(random.randint(1, 3))] for _ in range(n)]
        p = polynomial(cnf)
        w = resolution_width(cnf)
        roots_count = count_distinct_roots(p)
        
        results.append({
            "n": n,
            "roots_count": roots_count,
            "w": w
        })
    
    mean_roots_count = sum(result["roots_count"] for result in results) / len(results)
    mean_w = sum(result["w"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if abs(result["roots_count"] - 1.5 * result["w"]) <= 0.5 * result["w"]) / len(results)
    
    return {
        "metric_name": "Root Count vs Resolution Width",
        "metric_value": mean_roots_count,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"mean_roots_count={mean_roots_count}, mean_w={mean_w}"
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
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_roots_count does not satisfy the conjecture\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")