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
    
    def generate_sat_instance(n):
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(1, n + 1):
            clause = [random.choice([f"v{i}", f"-v{i}"]) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        cnf = [[c.split('v')[-1] if c.startswith('-') else c for c in clause] for clause in clauses]
        return cnf
    
    def indicator_polynomial(cnf):
        n = len(cnf[0])
        poly = [Fraction(1, 2)] * (n + 1)
        for clause in cnf:
            term = Fraction(1, 2)
            for literal in clause:
                if literal.startswith('-'):
                    var = int(literal[1:])
                    term *= Fraction(1 - poly[var], 2)
                else:
                    var = int(literal)
                    term *= Fraction(poly[var], 2)
            poly = [p + t * p_i for p, p_i in zip(poly, term)]
        return poly
    
    def tropical_abelianization(poly):
        n = len(poly) - 1
        abelian_poly = [0] * (n + 1)
        for i in range(n + 1):
            abelian_poly[i] = max([poly[j] + i - j for j in range(i + 1)])
        return abelian_poly
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        var = next((v for v in range(1, len(cnf[0]) + 1) if f"v{v}" not in [l for c in cnf for l in c] and f"-v{v}" not in [l for c in cnf for l in c]), None)
        if var is None:
            return False
        
        def extend_assignment(var, value):
            new_assignment = assignment[:]
            new_assignment.append((var, value))
            return new_assignment
        
        if dpll(cnf, extend_assignment(var, True)):
            return True
        if dpll(cnf, extend_assignment(var, False)):
            return True
        return False
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        cnf = generate_sat_instance(n_max)
        poly = indicator_polynomial(cnf)
        abelian_poly = tropical_abelianization(poly)
        ord_ab = max(abelian_poly)
        
        dlpl_length = len(dpll(cnf)) if dpll(cnf) else 0
        
        metric_values.append(ord_ab * dlpl_length)
    
    mean_value = sum(metric_values) / instances_tested
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in metric_values) / instances_tested)
    
    conjecture_holds = abs(mean_value) >= 0.7 * std_value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "ord_ab * dlpl_length",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
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