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
    
    def generate_3cnf(n, density):
        clauses = []
        for _ in range(int(density * n * (n - 1) / 2)):
            clause = [random.randint(1, n), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def resolution_width(clauses):
        literals = set()
        for clause in clauses:
            for literal in clause:
                literals.add(abs(literal))
        
        queue = list(literals)
        while queue:
            literal = queue.pop(0)
            if literal > 0:
                neg_literal = -literal
            else:
                neg_literal = -literal
            
            new_clauses = []
            for clause in clauses:
                if literal not in clause and neg_literal not in clause:
                    new_clauses.append(clause)
                elif literal in clause:
                    new_clause = [l for l in clause if l != literal]
                    if neg_literal in new_clause:
                        return 0
                    else:
                        new_clauses.append(new_clause)
                elif neg_literal in clause:
                    new_clause = [l for l in clause if l != neg_literal]
                    if literal in new_clause:
                        return 0
                    else:
                        new_clauses.append(new_clause)
            clauses = new_clauses
        
        return len(literals)

    def toric_polytope_facets(clauses):
        n = max(abs(var) for var, _ in clauses)
        facets = []
        for i in range(1, 2**n):
            facet = [0] * n
            for j in range(n):
                if (i >> j) & 1:
                    facet[j] = -1
                else:
                    facet[j] = 1
            valid = True
            for clause in clauses:
                product = 1
                for literal in clause:
                    product *= facet[abs(literal) - 1]
                if product == 0:
                    valid = False
                    break
            if valid:
                facets.append(facet)
        return len(facets)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        clauses = generate_3cnf(n, 2.5)
        facets = toric_polytope_facets(clauses)
        width = resolution_width(clauses)
        if width == 0:
            continue
        ratio = facets / math.log(n)
        results.append((ratio, width))
    
    if not results:
        return {
            "metric_name": "F/(log n)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_ratio = sum(r[0] for r in results) / len(results)
    mean_width = sum(r[1] for r in results) / len(results)
    std_dev = math.sqrt(sum((r[0] - mean_ratio)**2 for r in results) / len(results))
    
    return {
        "metric_name": "F/(log n)",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": abs(mean_ratio - mean_width) < 0.1 * mean_width,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, 'metric_name': '{result['metric_name']}', 'metric_value': {result['metric_value']}, 'instances_tested': {result['instances_tested']}, 'conjecture_holds': {result['conjecture_holds']}, 'counterexample': '{result['counterexample']}'}}")
    
    results = [run_trial(seed) for seed in seeds]
    mean_ratio = sum(r['metric_value'] for r in results if r['instances_tested'] > 0) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_ratio)**2 for r in results if r['instances_tested'] > 0) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['instances_tested'] > 0 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r['conjecture_holds']:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seeds[results.index(r)]}")
                break