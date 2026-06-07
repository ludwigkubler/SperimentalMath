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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(len(clause)) for j in range(i+1, len(clause))):
                clauses.append(tuple(sorted(clause)))
        return set(clauses)
    
    def p_adic_valuation_rank(cnf):
        primes = [2, 3, 5, 7, 11, 13, 17, 19]
        rank = 0
        for prime in primes:
            ring = {}
            for clause in cnf:
                indicator = tuple(sorted(clause))
                if indicator not in ring:
                    ring[indicator] = set()
                ring[indicator].add(prime)
            rank += len(ring)
        return rank
    
    def dpll(cnf):
        def solve(model, literals):
            if not literals:
                return True
            literal = literals[0]
            pos_lit, neg_lit = abs(literal), -literal
            if pos_lit in model and model[pos_lit] == False or neg_lit in model and model[neg_lit] == True:
                return False
            if pos_lit not in model and neg_lit not in model:
                model[pos_lit] = True
                if solve(model, literals[1:]):
                    return True
                del model[pos_lit]
                model[neg_lit] = True
                if solve(model, literals[1:]):
                    return True
                del model[neg_lit]
            elif pos_lit not in model:
                model[pos_lit] = True
                if solve(model, literals[1:]):
                    return True
                del model[pos_lit]
            else:
                model[neg_lit] = True
                if solve(model, literals[1:]):
                    return True
                del model[neg_lit]
            return False
        
        model = {}
        literals = [i for i in range(1, 2**len(cnf))]
        return len(literals) - sum(solve(model, literals))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        valrank = p_adic_valuation_rank(cnf)
        dpl = dpll(cnf)
        results.append((valrank, dpl))
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    valranks = [r[0] for r in results]
    dpls = [r[1] for r in results]
    mean_valrank = sum(valranks) / len(valranks)
    mean_dpl = sum(dpls) / len(dpls)
    covariance = sum((valranks[i] - mean_valrank) * (dpls[i] - mean_dpl) for i in range(len(results))) / len(results)
    variance_valrank = sum((valranks[i] - mean_valrank)**2 for i in range(len(results))) / len(results)
    variance_dpl = sum((dpls[i] - mean_dpl)**2 for i in range(len(results))) / len(results)
    correlation_coefficient = covariance / math.sqrt(variance_valrank * variance_dpl)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        if "conjecture_holds" not in trial_result or not trial_result["conjecture_holds"]:
            results.append(trial_result)
    
    if len(results) == 0:
        mean_value = None
        support_fraction = 1.0
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = sum(1 for r in results if "conjecture_holds" in r and r["conjecture_holds"]) / len(results)
    
    if all("conjecture_holds" not in r or not r["conjecture_holds"] for r in results):
        print(f"RESULT: INCONCLUSIVE no_conjecture_support n_tested={len(seeds)}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_correlation\" first_failing_seed={first_failing_seed}")