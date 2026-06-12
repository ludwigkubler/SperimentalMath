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
            if random.choice([True, False]):
                clause[0], clause[1] = clause[1], clause[0]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def solve(literals, clauses):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                if solve(literals + [literal], new_clauses):
                    return True
                else:
                    return solve(literals + [-literal], new_clauses)
            pure_literal = next((l for l in range(1, n+1) if (l in literals or -l in literals) and (-l not in literals or l not in literals)), None)
            if pure_literal is not None:
                literal = pure_literal
                new_clauses = [c for c in clauses if literal not in c and -literal not in c]
                if solve(literals + [literal], new_clauses):
                    return True
                else:
                    return solve(literals + [-literal], new_clauses)
            literal, _ = random.choice(clauses)
            new_clauses = [c for c in clauses if literal not in c and -literal not in c]
            return solve(literals + [literal], new_clauses) or solve(literals + [-literal], new_clauses)
        return solve([], cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        total_length = 0
        instances_tested = 0
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(2*n, 4*n))
            if not cnf:
                continue
            proof_length = len(dpll(cnf))
            total_length += proof_length
            instances_tested += 1
        if instances_tested == 0:
            return {
                "metric_name": "proof_length",
                "metric_value": float('nan'),
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "empty_cnf"
            }
        mean_length = total_length / instances_tested
        results.append(mean_length)
    
    if len(results) < 6:
        return {
            "metric_name": "proof_length",
            "metric_value": float('nan'),
            "instances_tested": sum(len(r) for r in results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_data"
        }
    
    mean_length = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean_length) ** 2 for x in results) / len(results))
    return {
        "metric_name": "proof_length",
        "metric_value": mean_length,
        "instances_tested": sum(len(r) for r in results),
        "n_max": max(n_values),
        "conjecture_holds": abs(mean_length - n**2 * math.log(n, 2)) <= 0.1 * abs(n**2 * math.log(n, 2)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if not result["conjecture_holds"]:
            break
    else:
        mean_length = sum(result["metric_value"] for result in results) / len(results)
        std_dev = math.sqrt(sum((result["metric_value"] - mean_length) ** 2 for result in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_length} std={std_dev} support_fraction={support_fraction}")