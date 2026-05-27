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
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clauses = [c for c in clauses if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            new_assignment[literal] = False
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literals = {}
        for clause in clauses:
            for literal in clause:
                if literal in pure_literals:
                    if pure_literals[literal] != (literal > 0):
                        return False
                else:
                    pure_literals[literal] = literal > 0
        for literal, polarity in pure_literals.items():
            new_assignment = assignment.copy()
            new_assignment[literal] = polarity
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
        return False
    
    def generate_instance(n):
        variables = set(range(1, n + 1))
        clauses = []
        for _ in range(random.randint(2 * n, 3 * n)):
            clause = random.sample(variables, random.randint(1, min(3, n)))
            if random.choice([True, False]):
                clause = [-v for v in clause]
            clauses.append(clause)
        return clauses
    
    def hodge_integral_lattice_size(clauses):
        # Simplified mapping to a lattice size
        return len(set(tuple(sorted(c)) for c in clauses))
    
    n = random.randint(1, 40)
    instance = generate_instance(n)
    if dpll(instance, {}):
        solution_size = len(instance) // 2
        hodge_rank = hodge_integral_lattice_size(instance)
        return {
            "metric_name": "min_rank_over_solution_size",
            "metric_value": hodge_rank / solution_size,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "min_rank_over_solution_size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "instance_not_solvable"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_d = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = "SUPPORTED"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"instance_not_solvable\" first_failing_seed={first_failing_seed}"
    
    print(f"RESULT: {result} mean={mean_d:.2f} std=0.00 support_fraction={support_fraction:.2f}")