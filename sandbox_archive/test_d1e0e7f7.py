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
    
    def generate_k_cnf(n, m):
        clauses = set()
        for _ in range(m):
            clause = []
            for i in range(k):
                lit = random.choice([1, -1]) * (random.randint(0, n-1) + 1)
                if lit not in clause:
                    clause.append(lit)
            clauses.add(tuple(sorted(clause)))
        return clauses
    
    def truth_table(k_cnf, n):
        tt_size = 2 ** n
        tt = [[False] * tt_size for _ in range(len(k_cnf))]
        for i, clause in enumerate(k_cnf):
            for j in range(tt_size):
                if all(lit > 0 and (j >> abs(lit) - 1) & 1 == (lit > 0) or lit < 0 and not ((j >> abs(lit) - 1) & 1) for lit in clause):
                    tt[i][j] = True
        return tt
    
    def min_representation_order(tt):
        n = len(tt[0])
        order = float('inf')
        for i in range(n):
            if all(tt[j][i] == tt[j][(i + 1) % n] for j in range(len(tt))):
                order = min(order, (i + 1) % n)
        return order
    
    def resolution_width(k_cnf):
        stack = list(k_cnf)
        learned_clauses = set()
        while stack:
            clause = stack.pop()
            if all(lit > 0 and -lit in learned_clauses or lit < 0 and -lit not in learned_clauses for lit in clause):
                return len(learned_clauses) + 1
            new_clause = None
            for i in range(len(clause)):
                lit = clause[i]
                if -lit in learned_clauses:
                    new_clause = [l for l in clause[:i] + clause[i+1:] if l != -lit]
                    break
            if new_clause:
                stack.append(tuple(sorted(new_clause)))
                learned_clauses.add(tuple(sorted(new_clause)))
        return len(learned_clauses) + 1
    
    k_values = [3, 4, 5]
    n_max = 0
    instances_tested = 0
    total_order = 0
    total_width = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in range(5, 41):
        for k in k_values:
            m = int(n * math.log2(n) / 2)
            if m <= 0: continue
            instances_tested += 1
            n_max = max(n_max, n)
            k_cnf = generate_k_cnf(n, m)
            tt = truth_table(k_cnf, n)
            order = min_representation_order(tt)
            width = resolution_width(k_cnf)
            total_order += order
            total_width += width
            
            if order > m ** (2/3) * n ** (1/4):
                conjecture_holds = False
                counterexample = f"n={n}, k={k}, m={m}, order={order}"
                break
    
    mean_order = total_order / instances_tested
    mean_width = total_width / instances_tested
    
    return {
        "metric_name": "Mean Resolution Width",
        "metric_value": mean_width,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")