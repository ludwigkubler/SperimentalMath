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
        literals = [f"x{i}" for i in range(1, n+1)]
        cnf = []
        for _ in range(m):
            clause = random.sample(literals, 2) + [random.choice(["~" + l for l in literals])]
            cnf.append(clause)
        return cnf
    
    def resolution_proof_size(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        unit_clauses = {c for c in clauses if len(c) == 1}
        while unit_clauses:
            new_clause = None
            for u in unit_clauses:
                for c in clauses:
                    if any(lit in c and "~" + lit not in c for lit in u):
                        new_clause = tuple(sorted([l for l in c if l != "~" + u[0]]))
                        break
                if new_clause:
                    break
            if new_clause:
                unit_clauses.add(new_clause)
                clauses.add(new_clause)
                unit_clauses.discard(u)
            else:
                return float('inf')
        return len(clauses) - len(unit_clauses)
    
    def generalized_continued_fraction(cnf):
        n = len(cnf[0])
        rank = 1
        for _ in range(n-1):
            rank *= (len(cnf) + rank)
        return rank
    
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        return abs(a*b) // gcd(a, b)
    
    def fraction_to_float(frac):
        if frac.denominator == 0:
            return float('inf')
        return float(frac.numerator / frac.denominator)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    total_rank = 0
    total_proof_size = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n*3))
            rank = generalized_continued_fraction(cnf)
            proof_size = resolution_proof_size(cnf)
            if proof_size == float('inf'):
                continue
            total_instances += 1
            total_rank += rank
            total_proof_size += proof_size
    
    mean_rank = total_rank / total_instances
    mean_proof_size = total_proof_size / total_instances
    correlation_coefficient = (total_instances * total_rank * total_proof_size - 
                               total_rank**2 * total_proof_size - 
                               total_rank * total_proof_size**2) / \
                              math.sqrt((total_instances * total_rank**2 - total_rank**4) *
                                        (total_instances * total_proof_size**2 - total_proof_size**4))
    
    conjecture_holds = correlation_coefficient >= 0.8 and all(proof_size <= rank * 1.5 for rank, proof_size in zip([mean_rank]*total_instances, [mean_proof_size]*total_instances))
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.8 or proof_size > rank * 1.5"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": total_instances,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric = sum(r["metric_value"] for r in results) / len(results)
    std_metric = math.sqrt(sum((r["metric_value"] - mean_metric)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric} std={std_metric} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")