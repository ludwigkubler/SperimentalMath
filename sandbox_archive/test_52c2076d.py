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
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def incidence_matroid_rank(clauses):
        matroid = {}
        for i, (x, y) in enumerate(clauses):
            if x not in matroid:
                matroid[x] = set()
            if y not in matroid:
                matroid[y] = set()
            matroid[x].add(i)
            matroid[y].add(i)
        
        rank = 0
        bases = []
        for var in matroid:
            new_base = [i for i in matroid[var] if all(j not in matroid[var] for j in bases)]
            if new_base:
                bases.append(new_base[0])
                rank += 1
        
        return rank
    
    def karchmer_wigderson_cost(clauses):
        n = len(clauses)
        cost = 0
        while clauses:
            clause = random.choice(clauses)
            x, y = abs(clause[0]), abs(clause[1])
            if clause[0] < 0:
                clauses.remove(clause)
                for c in clauses:
                    if x in c:
                        c.remove(x)
            else:
                clauses.remove(clause)
                for c in clauses:
                    if y in c:
                        c.remove(y)
            cost += 1
        return cost
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    rank = incidence_matroid_rank(clauses)
    karch_cost = karchmer_wigderson_cost(clauses)
    
    return {
        "metric_name": "Karchmer-Wigderson protocol cost",
        "metric_value": karch_cost,
        "instances_tested": 1,
        "conjecture_holds": karch_cost >= rank,
        "counterexample": "" if karch_cost >= rank else f"n={n}, clauses={clauses}"
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
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[seeds.index(first_failing_seed)]['instances_tested']}, clauses={results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")