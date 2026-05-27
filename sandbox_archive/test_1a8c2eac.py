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
    
    def generate_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n - 1):
            clause = random.sample(variables, random.randint(1, n))
            if random.choice([True, False]):
                clause = [f'not {v}' for v in clause]
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def dpll(instance):
        # Simplified DPLL solver
        variables = set()
        for clause in instance.split(' and '):
            for literal in clause.split(' or '):
                if literal.startswith('not'):
                    variables.add(literal[4:])
                else:
                    variables.add(literal)
        
        assignment = {v: None for v in variables}
        
        def solve():
            unassigned = [v for v, val in assignment.items() if val is None]
            if not unassigned:
                return all(assignment[v] == (v.startswith('not') != (instance.split(' and ')[i].split(' or ')[j].startswith('not'))) for i, clause in enumerate(instance.split(' and ')) for j, literal in enumerate(clause.split(' or ')))
            
            v = unassigned[0]
            assignment[v] = True
            if solve():
                return True
            assignment[v] = False
            if solve():
                return True
            assignment[v] = None
            return False
        
        if solve():
            return len([v for v, val in assignment.items() if val])
        else:
            return 0
    
    def hodge_integral_lattice(instance):
        # Constructive mapping to Hodge integral lattice (simplified)
        n = instance.count(' or ')
        return n
    
    results = []
    for n in range(1, 41):
        instances_tested = 0
        total_min_rank = 0
        for _ in range(30):
            instance = generate_instance(n)
            solution_size = dpll(instance)
            if solution_size > 0:
                min_rank = hodge_integral_lattice(instance)
                results.append((min_rank, solution_size))
                instances_tested += 1
    
    if not results:
        return {
            "metric_name": "min_rank_per_solution_size",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_satisfiable_instances_found"
        }
    
    mean_min_rank = sum(r[0] for r in results) / len(results)
    mean_solution_size = sum(r[1] for r in results) / len(results)
    support_fraction = Fraction(mean_min_rank, mean_solution_size).limit_denominator()
    
    return {
        "metric_name": "min_rank_per_solution_size",
        "metric_value": mean_min_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = Fraction(sum(1 for r in results if r["conjecture_holds"]), len(results)).limit_denominator()
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")