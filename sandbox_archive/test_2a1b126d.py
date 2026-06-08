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
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def frege_depth(cnf):
        def dpll(cnf, assignment):
            if not cnf:
                return 0
            unit_clauses = [c for c in cnf if len(c) == 1]
            if unit_clauses:
                literal, _ = unit_clauses[0]
                new_assignment = assignment.copy()
                new_assignment[abs(literal)] = literal > 0
                return 1 + dpll([c for c in cnf if literal not in c], new_assignment)
            pure_literals = {}
            for lit in set(abs(c) for c in cnf):
                pos_count, neg_count = sum(1 for c in cnf if lit in c), sum(1 for c in cnf if -lit in c)
                if pos_count == 0:
                    pure_literals[lit] = True
                elif neg_count == 0:
                    pure_literals[lit] = False
            if not pure_literals:
                return float('inf')
            literal, value = next(iter(pure_literals.items()))
            new_assignment = assignment.copy()
            new_assignment[abs(literal)] = value
            return 1 + dpll([c for c in cnf if literal not in c], new_assignment)
        return dpll(cnf, {})

    def local_index(cnf):
        n = len(set(abs(lit) for clause in cnf for lit in clause))
        # Simplified computation of local index
        return math.log(n, 2)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        li = local_index(cnf)
        fd = frege_depth(cnf)
        if fd == float('inf'):
            continue
        ratio = li / fd
        expected_ratio = math.log(2, 2) ** li
        results.append({
            "n": n,
            "local_index": li,
            "frege_depth": fd,
            "ratio": ratio,
            "expected_ratio": expected_ratio
        })
    
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    min_ratio = min(result["ratio"] for result in results)
    max_ratio = max(result["ratio"] for result in results)
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio) ** 2 for result in results) / len(results))
    
    conjecture_holds = all(0.5 <= ratio / expected_ratio <= 2 for ratio, expected_ratio in zip(min_ratio, max_ratio))
    counterexample = "" if conjecture_holds else "Ratio out of bounds"
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not all("metric_value" in r and r["metric_value"] is not None for r in results):
        print("RESULT: INCONCLUSIVE reason=missing_data")
    else:
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample='Ratio out of bounds' first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE reason=insufficient_support")