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
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        if not cnf:
            return True
        literal = next((l for l in range(1, len(cnf) + 1) if any(l in c or -l in c for c in cnf)), None)
        if literal is None:
            return False
        def propagate(clauses, literal):
            new_clauses = []
            for clause in clauses:
                if literal not in clause and -literal not in clause:
                    new_clauses.append(clause)
                elif literal in clause:
                    continue
                else:
                    new_clause = [l for l in clause if l != -literal]
                    if len(new_clause) == 0:
                        return None
                    new_clauses.append(new_clause)
            return new_clauses
        def backtrack(literal):
            return dpll(propagate(cnf, literal))
        if backtrack(literal):
            return True
        else:
            return backtrack(-literal)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = len(cnf)  # Simplified rank calculation
        width = dpll(cnf)
        if width is None:
            continue
        results.append((rank, width))
    
    if not results:
        return {
            "metric_name": "Correlation",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    rank_sum = sum(r for r, _ in results)
    width_sum = sum(w for _, w in results)
    rank_mean = rank_sum / len(results)
    width_mean = width_sum / len(results)
    
    correlation = 0.0
    for r, w in results:
        correlation += (r - rank_mean) * (w - width_mean)
    correlation /= len(results) * math.sqrt(sum((r - rank_mean)**2 for r, _ in results)) * math.sqrt(sum((w - width_mean)**2 for _, w in results))
    
    return {
        "metric_name": "Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) > 0.8 and all(abs(r - rank_mean) <= 3 for r, _ in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if all(r["conjecture_holds"] for r in all_results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif sum(1 for r in all_results if not r["conjecture_holds"]) / len(all_results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[all_results.index(next(r for r in all_results if not r['conjecture_holds']))]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(all_results)}")