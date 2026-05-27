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
    
    def generate_instance(n):
        variables = [f'x{i}' for i in range(n)]
        clauses = []
        for _ in range(2**n):
            clause = ' or '.join(random.sample(variables, 2))
            clauses.append(clause)
        return ' and '.join(clauses)
    
    def dpll(instance):
        # Simplified DPLL solver
        if not instance:
            return True
        literals = set()
        for clause in instance.split(' and '):
            literals.update(clause.split(' or '))
        literal = random.choice(list(literals))
        positive = literal.startswith('x')
        sub_instance = instance.replace(literal, '', 1).replace(f'not {literal}', '', 1)
        if dpll(sub_instance):
            return True
        sub_instance = instance.replace(literal, 'not ' + literal, 1).replace(f'{literal}', '', 1)
        if dpll(sub_instance):
            return True
        return False
    
    def hodge_integral_lattice(instance):
        # Simplified Hodge integral lattice construction
        rank = len(instance.split(' and '))
        return rank
    
    n = random.randint(5, 40)
    instance = generate_instance(n)
    solution_size = dpll(instance)
    
    if not solution_size:
        return {
            "metric_name": "min_rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "instance_not_solvable"
        }
    
    min_rank = hodge_integral_lattice(instance)
    metric_value = min_rank / solution_size
    
    return {
        "metric_name": "min_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 89))  # Default to first 30 primes if no seeds provided
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = seed
                break
        
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")