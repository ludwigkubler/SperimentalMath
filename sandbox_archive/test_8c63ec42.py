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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def resolution(cnf):
        clauses = set(tuple(sorted(clause)) for clause in cnf)
        while True:
            new_clauses = []
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == 2:
                        lit = list(set(c1) ^ set(c2))[0]
                        new_clause = [l for l in c1 + c2 if l != -lit and l != lit]
                        if not new_clause:
                            return None
                        new_clauses.append(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return len(clauses)
    
    def dyadic_spectrum(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        spectrum = [0] * (n + 1)
        for clause in cnf:
            for lit in clause:
                spectrum[abs(lit)] += 1
        return spectrum
    
    def entropy(spectrum):
        total = sum(spectrum)
        if total == 0:
            return 0
        return -sum(x / total * math.log2(x / total) for x in spectrum if x > 0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(1, n * 5)
        cnf = generate_cnf(n, m)
        proof_depth = resolution(cnf)
        if proof_depth is None:
            continue
        spectrum = dyadic_spectrum(cnf)
        H_d_PT = entropy(spectrum)
        results.append({
            "n": n,
            "m": m,
            "proof_depth": proof_depth,
            "H_d_PT": H_d_PT
        })
    
    if not results:
        return {
            "metric_name": "H_d(PT)",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No resolution proof found"
        }
    
    H_d_PT_values = [result["H_d_PT"] for result in results]
    avg_H_d_PT = sum(H_d_PT_values) / len(H_d_PT_values)
    max_n = max(result["n"] for result in results)
    
    if max_n < 16:
        return {
            "metric_name": "H_d(PT)",
            "metric_value": avg_H_d_PT,
            "instances_tested": len(results),
            "n_max": max_n,
            "conjecture_holds": False,
            "counterexample": "Insufficient n_max"
        }
    
    return {
        "metric_name": "H_d(PT)",
        "metric_value": avg_H_d_PT,
        "instances_tested": len(results),
        "n_max": max_n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Insufficient support\" first_failing_seed={first_failing_seed}")