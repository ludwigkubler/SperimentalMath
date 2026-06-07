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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(10 * n):  # Generate 10n clauses to ensure variety
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause.append(-1)
            clauses.append(clause)
        return clauses

    def p_adic_valuation_rank(cnf):
        primes = [2] + [i for i in range(3, 50, 2) if all(i % p != 0 for p in primes)]
        rank = 0
        for clause in cnf:
            indicators = set()
            for literal in clause:
                if literal > 0:
                    indicators.add(literal)
                else:
                    indicators.add(-literal)
            prime_ideals = []
            for prime in primes:
                if all(indicator % prime != 0 for indicator in indicators):
                    prime_ideals.append(prime)
            rank = max(rank, len(prime_ideals))
        return rank

    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        literal = next((l for l in range(1, 2 * n + 1) if l not in assignment and -l not in assignment), None)
        if literal is None:
            return False
        
        def propagate(lit):
            new_cnf = []
            for clause in cnf:
                if lit in clause:
                    continue
                elif -lit in clause:
                    new_clause = [x for x in clause if x != -lit]
                    if not new_clause:
                        return None
                    new_cnf.append(new_clause)
                else:
                    new_cnf.append(clause)
            return new_cnf
        
        def backtrack():
            return dpll(cnf, assignment[:-1])
        
        if propagate(literal) is not None:
            if dpll(propagate(literal), assignment + [literal]):
                return True
        if propagate(-literal) is not None:
            if dpll(propagate(-literal), assignment + [-literal]):
                return True
        return backtrack()
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        valrank = p_adic_valuation_rank(cnf)
        dpl = 0
        if dpll(cnf):
            dpl = len(assignment)  # This is a simplified DPLL implementation, so the path length might be an overestimate.
        
        results.append({
            "n": n,
            "valrank": valrank,
            "dpl": dpl
        })
    
    if not results:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    valranks = [result["valrank"] for result in results]
    dpls = [result["dpl"] for result in results]
    
    def pearson_correlation(x, y):
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        cov_xy = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n)) / n
        std_x = (sum((x[i] - mean_x) ** 2 for i in range(n)) / n) ** 0.5
        std_y = (sum((y[i] - mean_y) ** 2 for i in range(n)) / n) ** 0.5
        return cov_xy / (std_x * std_y)
    
    r = pearson_correlation(valranks, dpls)
    p_value = None  # Computing p-value is complex and not feasible within the constraints.
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": r,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(r) > 0.8,
        "counterexample": "" if abs(r) > 0.8 else "p-value not computed"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if abs(r["metric_value"]) > 0.8) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r} std=Unknown support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"p-value not computed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=Unknown")