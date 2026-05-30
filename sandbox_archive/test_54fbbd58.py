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
    
    def resolution_proof_depth(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        depth = 0
        while True:
            new_clauses = []
            for c1 in clauses:
                for c2 in clauses:
                    if len(set(c1) & set(c2)) == 2:
                        lit = list(set(c1) ^ set(c2))[0]
                        new_clause = [lit] + [l for l in c1 if l != -lit]
                        new_clauses.append(new_clause)
            if not new_clauses:
                break
            clauses.update(tuple(sorted(c)) for c in new_clauses)
            depth += 1
        return depth
    
    def dyadic_spectrum(clause):
        n = len(clause)
        spectrum = [0] * (n + 1)
        for i in range(n):
            spectrum[i % (n + 1)] += abs(clause[i])
        return spectrum
    
    def entropy(spectrum):
        total = sum(spectrum)
        if total == 0:
            return 0
        return -sum(x / total * math.log2(x / total) for x in spectrum if x > 0)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        m = random.randint(1, n * 2)
        cnf = generate_cnf(n, m)
        depth = resolution_proof_depth(cnf)
        spectrum = dyadic_spectrum(cnf)
        H_d = entropy(spectrum)
        results.append({
            "n": n,
            "m": m,
            "depth": depth,
            "H_d": H_d
        })
    
    mean_H_d = sum(r["H_d"] for r in results) / len(results)
    std_H_d = math.sqrt(sum((r["H_d"] - mean_H_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["H_d"] <= 0.5 * math.log2(r["m"] + r["n"])) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else f"H_d = {mean_H_d}, m+n = {sum(r['m'] + r['n'] for r in results) / len(results)}"
    
    return {
        "metric_name": "H_d",
        "metric_value": mean_H_d,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_H_d = sum(r["metric_value"] for r in results) / len(results)
    std_H_d = math.sqrt(sum((r["metric_value"] - mean_H_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_H_d} std={std_H_d} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")