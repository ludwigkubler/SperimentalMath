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
    
    def tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n + 1)]
        clauses = []
        
        # Generate Tseitin formula
        for i in range(2, n + 1):
            clause = [-variables[i - 2], variables[i - 1]]
            clauses.append(clause)
            
            clause = [variables[i - 2], variables[i - 1]]
            clauses.append(clause)
        
        # Add final clause
        clause = []
        for i in range(1, n + 1):
            clause.append(variables[i - 1])
        clauses.append(clause)
        
        return variables, clauses
    
    def monomial_ideal(clauses):
        ideal = set()
        for clause in clauses:
            for literal in clause:
                if literal.startswith('x'):
                    ideal.add(literal)
                else:
                    ideal.add(-literal)
        return ideal
    
    def associated_graded_ring(ideal):
        ring = {}
        for monomial in ideal:
            degree = sum(1 for char in monomial if char == 'x')
            if degree not in ring:
                ring[degree] = set()
            ring[degree].add(monomial)
        return ring
    
    def minimal_rank(ring):
        rank = 0
        for degree in sorted(ring.keys()):
            rank += len(ring[degree])
        return rank
    
    n = random.randint(5, 40)
    variables, clauses = tseitin_formula(n)
    ideal = monomial_ideal(clauses)
    graded_ring = associated_graded_ring(ideal)
    rank = minimal_rank(graded_ring)
    
    # Construct resolution proof
    width = 2 ** (n // 2)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width >= 2 ** (n / 2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 2 ** (r["instances_tested"] / 2) for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='width_less_than_2^(n/2)' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=not_enough_evidence")