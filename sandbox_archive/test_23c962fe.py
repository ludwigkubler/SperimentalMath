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
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        var = next(iter(clauses[0]))
        for val in [True, False]:
            new_assignment = assignment.copy()
            new_assignment[var] = val
            if all(any(new_assignment[v] == literal for v, literal in clause.items()) for clause in clauses):
                if dpll([clause - {var: literal} for clause in clauses if var in clause], new_assignment):
                    return True
        return False
    
    def generate_sat_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = {}
            for v in random.sample(variables, random.randint(1, n)):
                clause[v] = random.choice([True, False])
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses):
        poly = {(): 1}
        for clause in clauses:
            new_poly = {}
            for term, coeff in poly.items():
                for var, literal in clause.items():
                    if literal:
                        new_term = term + (var,)
                    else:
                        new_term = tuple(v for v in term if v != var)
                    new_poly[new_term] = coeff
            poly = new_poly
        return poly
    
    def minimal_representation_length(poly):
        length = 0
        for term, coeff in poly.items():
            length += len(term) * abs(coeff)
        return length
    
    def distinct_brauer_groups(clauses):
        groups = set()
        for clause in clauses:
            group = tuple(sorted(clause.keys()))
            groups.add(group)
        return len(groups)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_length = 0
        total_brauer_groups = 0
        
        while instances_tested < 30:
            clauses = generate_sat_instance(n)
            poly = clause_indicator_polynomial(clauses)
            length = minimal_representation_length(poly)
            num_brauer_groups = distinct_brauer_groups(clauses)
            
            if length > 0 and num_brauer_groups > 0:
                instances_tested += 1
                total_length += length
                total_brauer_groups += num_brauer_groups
        
        if instances_tested < 30:
            return {
                "metric_name": "minimal_representation_length",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
        
        avg_length = total_length / instances_tested
        avg_brauer_groups = total_brauer_groups / instances_tested
        expected_length = math.log(n) * avg_brauer_groups
        
        results.append({
            "n": n,
            "avg_length": avg_length,
            "expected_length": expected_length,
            "ratio": avg_length / expected_length if expected_length > 0 else float('inf')
        })
    
    mean_ratio = sum(result['ratio'] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result['ratio'] - mean_ratio) ** 2 for result in results) / len(results))
    
    return {
        "metric_name": "minimal_representation_length",
        "metric_value": mean_ratio,
        "instances_tested": sum(result['instances_tested'] for result in results),
        "n_max": max(result['n'] for result in results),
        "conjecture_holds": all(0.5 <= ratio <= 2 for ratio in [result['ratio'] for result in results]),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(result['metric_value'] for result in results if result['conjecture_holds']) / sum(result['instances_tested'] for result in results if result['conjecture_holds'])
    std_ratio = math.sqrt(sum((result['metric_value'] - mean_ratio) ** 2 for result in results if result['conjecture_holds']) / sum(result['instances_tested'] for result in results if result['conjecture_holds']))
    
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"insufficient_evidence\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")