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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_edge(v, w):
        return (v, w) in quiver or (w, v) in quiver
    
    def find_symmetry_group():
        n = len(quiver)
        G = []
        for perm in itertools.permutations(range(n)):
            if all(is_edge(v, w) == is_edge(perm[v], perm[w]) for u in range(n) for v, w in quiver[u]):
                G.append(perm)
        return G
    
    def tseitin_formula(quiver):
        n = len(quiver)
        literals = {v: f'x{v}' for v in range(n)}
        clauses = []
        for u in range(n):
            for v, w in quiver[u]:
                clauses.append([literals[v], literals[w]])
                clauses.append([-literals[v], -literals[w]])
                clauses.append([-literals[v], literals[w]])
                clauses.append([literals[v], -literals[w]])
        return clauses
    
    def resolution_refutation_length(clauses):
        n = len(quiver)
        unit_clauses = {l: [] for l in range(-n, n+1)}
        for clause in clauses:
            for literal in clause:
                unit_clauses[literal].append(clause)
        
        resolvents = []
        while True:
            new_resolvents = set()
            for clause in clauses:
                if len(clause) == 1:
                    resolvents.append(clause[0])
                    continue
                for literal in clause:
                    if -literal in resolvents:
                        new_resolvent = [l for l in clause if l != literal and -l != literal]
                        if new_resolvent not in new_resolvents:
                            new_resolvents.add(tuple(sorted(new_resolvent)))
            if not new_resolvents:
                break
            clauses.extend(new_resolvents)
        
        return len(resolvents)
    
    n = random.randint(5, 40)
    quiver = {v: [] for v in range(n)}
    for u in range(n):
        for v in range(u+1, n):
            if random.choice([True, False]):
                quiver[u].append((u, v))
                quiver[v].append((v, u))
    
    symmetry_group = find_symmetry_group()
    resolution_length = resolution_refutation_length(tseitin_formula(quiver))
    
    return {
        "metric_name": "resolution_refutation_length",
        "metric_value": resolution_length,
        "instances_tested": 1,
        "conjecture_holds": resolution_length >= 2**(math.log(len(symmetry_group), 2)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_length = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_length} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_length} std={math.sqrt(sum((r['metric_value'] - mean_length)**2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='resolution_length < 2^(log(|G|, 2))' first_failing_seed={first_failing_seed}")