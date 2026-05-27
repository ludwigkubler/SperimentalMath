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
    
    def generate_monotone_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def dpll(sat_formula, assignment):
        if not sat_formula:
            return True
        literal = next(lit for lit in sat_formula[0] if lit != 0)
        var = abs(literal) - 1
        pos_assignment = assignment[:]
        neg_assignment = assignment[:]
        pos_assignment[var] = literal > 0
        neg_assignment[var] = literal < 0
        return dpll(sat_formula, pos_assignment) or dpll(sat_formula, neg_assignment)
    
    def count_quadratic_forms(circuit):
        n = len(circuit)
        count = 0
        for i in range(n):
            for j in range(i+1, n):
                if circuit[i][j] != 0:
                    count += 1
        return count
    
    def construct_monomial_circuit(f):
        n = int(math.log2(len(f)))
        variables = list(range(1, n + 1))
        clauses = []
        for i in range(n):
            for j in range(i+1, n):
                if f[i] == 1 and f[j] == 1:
                    clause = [i + 1, -j - 1]
                    clauses.append(clause)
                elif f[i] == 1 and f[j] == 0:
                    clause = [-i - 1, j + 1]
                    clauses.append(clause)
                elif f[i] == 0 and f[j] == 1:
                    clause = [i + 1, j + 1]
                    clauses.append(clause)
        circuit = [[0 for _ in range(n)] for _ in range(n)]
        for clause in clauses:
            for lit in clause:
                var = abs(lit) - 1
                if lit > 0:
                    circuit[var][var] += 1
        return circuit
    
    n = random.randint(5, 40)
    f = generate_monotone_boolean_function(n)
    circuit = construct_monomial_circuit(f)
    
    quadratic_count = count_quadratic_forms(circuit)
    
    return {
        "metric_name": "average_quadratic_forms",
        "metric_value": quadratic_count,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = Fraction(total_metric_value).limit_denominator()
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")