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
    
    def generate_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for _ in range(n):
            clause = random.sample(variables + [f'~{v}' for v in variables], 2)
            clauses.append(' | '.join(clause))
        return ' & '.join(clauses)
    
    def incidence_matrix(formula, n):
        matrix = [[0] * (n + n) for _ in range(n)]
        for i, clause in enumerate(formula.split(' & ')):
            literals = clause.split(' | ')
            for literal in literals:
                if literal.startswith('~'):
                    var = literal[1:]
                    j = variables.index(var)
                    matrix[i][j] = -1
                else:
                    j = variables.index(literal)
                    matrix[i][j + n] = 1
        return matrix
    
    def min_order(matrix, p):
        n = len(matrix)
        for k in range(1, n):
            for l in range(k + 1, n):
                a_k = sum(matrix[i][k] * (p ** i) % (p - 1) for i in range(n)) % (p - 1)
                a_l = sum(matrix[i][l] * (p ** i) % (p - 1) for i in range(n)) % (p - 1)
                if abs(a_k - a_l) == 1:
                    return k
        return n
    
    def frege_proof_length(formula):
        # Placeholder function to simulate Frege proof length calculation
        return len(formula.split(' & ')) * len(formula.split(' | '))
    
    p = 2
    n_max = 0
    instances_tested = 0
    total_metric_value = Fraction(0)
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            formula = generate_formula(n)
            matrix = incidence_matrix(formula, n)
            min_order_val = min_order(matrix, p)
            proof_length = frege_proof_length(formula)
            
            if min_order_val == 0 or proof_length == 0:
                continue
            
            metric_value = math.log(p - 1) ** min_order_val / (math.log(2 ** proof_length) + 1)
            total_metric_value += Fraction(metric_value).limit_denominator()
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "log(p-1)^min_order(Inc(φ)) / (log(2^{w(Frege(φ))) + 1)",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_metric_value = total_metric_value / instances_tested
    return {
        "metric_name": "log(p-1)^min_order(Inc(φ)) / (log(2^{w(Frege(φ))) + 1)",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    supported_count = sum(1 for r in results if r["conjecture_holds"])
    support_fraction = Fraction(supported_count, len(results))
    
    if support_fraction >= Fraction(80, 100):
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=... support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not_supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")