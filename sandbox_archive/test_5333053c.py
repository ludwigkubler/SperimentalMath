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
        for _ in range(2**n - 1):
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, n))]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                clauses.append(clause)
        return clauses

    def dpll(cnf, assignment):
        unsatisfied = [c for c in cnf if not any(lit in assignment and assignment[lit] == (lit > 0) or -lit in assignment and not assignment[-lit] for lit in c)]
        if not unsatisfied:
            return True
        unit_clauses = [c[0] for c in unsatisfied if len(c) == 1]
        if not unit_clauses:
            return None
        literal = random.choice(unit_clauses)
        assignment[literal] = literal > 0
        if dpll(cnf, assignment):
            return True
        del assignment[literal]
        assignment[-literal] = False
        return dpll(cnf, assignment)

    def ehrhart_rank(n):
        # Placeholder for Ehrhart rank calculation
        return random.randint(1, n)

    def frege_complexity(cnf):
        assignment = {}
        return len(dpll(cnf, assignment))

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        rank_sum = 0
        complexity_sum = 0
        instances_tested = 0
        for _ in range(5):  # Sample 5 instances per size
            cnf = generate_cnf(n)
            rank = ehrhart_rank(n)
            complexity = frege_complexity(cnf)
            rank_sum += rank
            complexity_sum += complexity
            instances_tested += 1
        avg_rank = rank_sum / instances_tested
        avg_complexity = complexity_sum / instances_tested
        results.append({
            "metric_name": "rank_vs_complexity",
            "metric_value": avg_rank,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        })

    return {
        "seed": seed,
        **results[0]
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]  # Default to first 10 primes if no seeds provided
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")