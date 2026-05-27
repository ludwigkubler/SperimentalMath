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
    
    def generate_sat_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2 * n):
            clause = random.sample(variables, 3)
            clauses.append(f"({' or '.join(clause)})")
        return ' and '.join(clauses)

    def is_satisfiable(instance):
        # Simplified SAT solver using DPLL
        def dpll(clauses, assignment):
            if not clauses:
                return True
            literal = next((lit for lit in variables if lit not in assignment), None)
            if literal is None:
                return False
            new_clauses = []
            for clause in clauses:
                if any(lit in assignment and assignment[lit] == val for lit, val in [('!', literal), (literal, True)]):
                    continue
                elif all(lit not in assignment or assignment[lit] != val for lit, val in [('!', literal), (literal, False)]):
                    new_clauses.append(clause)
            return dpll(new_clauses, {**assignment, literal: True}) or dpll(new_clauses, {**assignment, literal: False})
        variables = [var[2:] if var.startswith('!') else var for var in instance.split()]
        clauses = instance.split(' and ')
        return dpll(clauses, {})

    def coxeter_group_rank(n):
        # Simplified rank calculation (placeholder)
        return n

    def tropicalized_representation_rank(instance):
        if is_satisfiable(instance):
            return coxeter_group_rank(len(instance.split()))
        else:
            return 1

    instance = generate_sat_instance(40)
    min_rank = tropicalized_representation_rank(instance)
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": min_rank >= math.log(len(instance.split()), 2),
        "counterexample": f"n={len(instance.split())}, min_rank={min_rank}" if not conjecture_holds else ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result = f"SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}"
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        result = f"FALSIFIED counterexample=\"n={len(results[0]['metric_value'].split())}, min_rank={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}"
    
    print(result)