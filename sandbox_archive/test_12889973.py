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
        for i in range(2**n):
            clause = [random.choice([-1, 1]) * (j + 1) for j in range(n)]
            if all(clause[j] != -clause[(j + 1) % n] for j in range(n)):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        clauses = cnf[:]
        while True:
            new_clauses = []
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    if any(abs(x) == abs(y) and (x > 0) != (y > 0) for x in clauses[i] for y in clauses[j]):
                        new_clause = [lit for lit in clauses[i] if lit not in clauses[j] and -lit not in clauses[j]]
                        if new_clause:
                            new_clauses.append(new_clause)
            if not new_clauses:
                return len(clauses)
            clauses.extend(new_clauses)
    
    def noncommutative_crossed_product(cnf):
        n = int(math.log2(len(cnf[0])))
        G_f = []
        for clause in cnf:
            row = [0] * (2**n)
            for lit in clause:
                if lit > 0:
                    row[lit - 1] += 1
                else:
                    row[-lit - 1] -= 1
            G_f.append(row)
        return G_f
    
    def min_rank(G):
        m, n = len(G), len(G[0])
        rank = 0
        for i in range(m):
            if any(G[i][j] != 0 for j in range(n)):
                rank += 1
                for j in range(n):
                    if G[i][j] != 0:
                        factor = G[i][j]
                        for k in range(m):
                            G[k][j] -= G[k][i] * (G[k][j] // factor)
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        G_f = noncommutative_crossed_product(cnf)
        r_G_f = min_rank(G_f)
        w_CNF_f = resolution_width(cnf)
        
        if w_CNF_f == 0:
            continue
        
        results.append((r_G_f, w_CNF_f))
    
    if not results:
        return {
            "metric_name": "min_rank_over_resolution_width",
            "metric_value": float('inf'),
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": "No valid CNF found"
        }
    
    r_G_f_avg = sum(r for r, _ in results) / len(results)
    w_CNF_f_avg = sum(w for _, w in results) / len(results)
    c = r_G_f_avg / w_CNF_f_avg
    
    support_fraction = sum(1 for r, w in results if r <= c * w) / len(results)
    
    return {
        "metric_name": "min_rank_over_resolution_width",
        "metric_value": c,
        "instances_tested": len(n_values),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"c={c}, r_G_f_avg={r_G_f_avg}, w_CNF_f_avg={w_CNF_f_avg}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in r or r["conjecture_holds"] for r in results):
        RESULT = "SUPPORTED"
    elif any("counterexample" in r and r["counterexample"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if "counterexample" in r and r["counterexample"])
        RESULT = f"FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE"
    
    print(f"RESULT: {RESULT} mean=<x> std=<y> support_fraction=<z>")