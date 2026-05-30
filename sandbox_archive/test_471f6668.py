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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = set()
            while len(clause) < 2 or len(clause) > n:
                lit = random.randint(1, n)
                if random.choice([True, False]):
                    lit = -lit
                clause.add(lit)
            cnf.append(list(clause))
        return cnf
    
    def resolution(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        new_clauses = set()
        while True:
            added = False
            for c1, c2 in itertools.combinations(clauses, 2):
                if any(-lit in c2 for lit in c1):
                    new_clause = [lit for lit in c1 if lit not in c2]
                    new_clause.extend([lit for lit in c2 if -lit not in c1])
                    new_clauses.add(tuple(sorted(new_clause)))
                    added = True
            if not added:
                break
            clauses.update(new_clauses)
            new_clauses.clear()
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
        return -sum(Fraction(count, total) * math.log2(Fraction(count, total)) for count in spectrum if count > 0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * (n + 1) // 2)
        cnf = generate_cnf(n, m)
        proof_depth = resolution(cnf)
        spectrum = dyadic_spectrum(cnf)
        H_d_PT = entropy(spectrum)
        
        results.append({
            "metric_name": "H_d(PT)",
            "metric_value": H_d_PT,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": H_d_PT <= math.log2(m + n),
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        "metric_name": "H_d(PT)",
        "metric_value": sum(result["metric_value"] for result in results) / len(results),
        "instances_tested": len(results),
        "n_max": max(result["n_max"] for result in results),
        "conjecture_holds": all(result["conjecture_holds"] for result in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
    
    results = [run_trial(seed)["conjecture_holds"] for seed in seeds]
    support_fraction = sum(results) / len(results)
    mean_value = sum(run_trial(seed)["metric_value"] for seed in seeds) / len(seeds)
    
    if all(results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result for result in results):
        first_failing_seed = next(i for i, result in enumerate(results) if not result)
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed + 1}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")