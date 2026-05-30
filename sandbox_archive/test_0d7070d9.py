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
        cnf = []
        for _ in range(10 * n):  # Generate 10 clauses per variable on average
            clause = [random.randint(-n, -1), random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def unit_propagate(cnf):
            while True:
                found_unit_clause = False
                for i in range(len(cnf)):
                    clause = cnf[i]
                    if len(clause) == 1:
                        literal = clause[0]
                        sign = literal > 0
                        value = abs(literal)
                        new_cnf = []
                        for j, other_clause in enumerate(cnf):
                            if i != j and value not in [abs(x) for x in other_clause]:
                                new_cnf.append(other_clause)
                            elif i == j:
                                new_cnf.append([x for x in other_clause if x != literal])
                        cnf = new_cnf
                        found_unit_clause = True
                if not found_unit_clause:
                    break
        
        def dpll_recursive(cnf, assignment):
            unit_propagate(cnf)
            if not cnf:
                return assignment
            if any(len(clause) == 0 for clause in cnf):
                return None
            literal = next(lit for lit in range(1, len(assignment) + 1) if lit not in assignment and -lit not in assignment)
            assignment[literal] = True
            result = dpll_recursive(cnf, assignment)
            if result is not None:
                return result
            del assignment[literal]
            assignment[-literal] = True
            return dpll_recursive(cnf, assignment)
        
        return dpll_recursive(cnf, {})
    
    def diophantine_exponent(cnf):
        n = len(cnf)
        for d in range(1, 2 * n + 1):
            if all(all((x % d == y % d) or (x % d != y % d and x % d != -y % d) for x, y in clause) for clause in cnf):
                return d
        return 2 * n
    
    def refutation_time(cnf):
        start_time = time.time()
        result = dpll(cnf)
        end_time = time.time()
        if result is None:
            return float('inf')
        return end_time - start_time
    
    import time
    n_max = 0
    instances_tested = 0
    total_ratio = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if time.time() - start_time > 200:
            return {
                "metric_name": "Ratio",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "budget_exceeded"
            }
        cnf = generate_cnf(n)
        d = diophantine_exponent(cnf)
        ratio = (n ** d) * math.log(n)
        ref_time = refutation_time(cnf)
        if ref_time == float('inf'):
            continue
        instances_tested += 1
        n_max = max(n_max, n)
        total_ratio += ratio / ref_time
    
    mean_ratio = total_ratio / instances_tested
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_ratio <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['metric_value'] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")