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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n * (n - 1)):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def construct_stabilizer_state(cnf):
        n = len(set(abs(lit) for lit in cnf))
        state = [0] * (2 ** n)
        for clause in cnf:
            product = 1
            for lit in clause:
                if lit > 0:
                    product *= (1 + 1j) ** (lit - 1)
                else:
                    product *= (1 - 1j) ** (-lit - 1)
            state[product.real] += 1
        return state
    
    def calculate_entanglement_entropy(state):
        n = len(state)
        probabilities = [abs(x) ** 2 for x in state]
        entropy = sum(-p * math.log2(p) if p > 0 else 0 for p in probabilities)
        return entropy
    
    def resolution_width(cnf):
        width = 1
        queue = cnf[:]
        while queue:
            clause = queue.pop(0)
            new_clauses = []
            for other_clause in queue:
                common_lits = set(lit for lit in clause if -lit in other_clause)
                if len(common_lits) == 1:
                    new_lit = random.choice(list(common_lits))
                    new_clauses.append([new_lit, -new_lit])
            width = max(width, len(queue) + len(new_clauses))
            queue.extend(new_clauses)
        return width
    
    n_max = 40
    instances_tested = 30
    total_width = 0
    total_entropy = 0
    
    for _ in range(instances_tested):
        n = random.randint(5, n_max)
        cnf = generate_cnf(n)
        state = construct_stabilizer_state(cnf)
        entropy = calculate_entanglement_entropy(state)
        width = resolution_width(cnf)
        
        total_width += width
        total_entropy += entropy
    
    mean_width = total_width / instances_tested
    mean_entropy = total_entropy / instances_tested
    
    correlation_coefficient = (instances_tested * sum(w * e for w, e in zip(range(5, n_max + 1), range(5, n_max + 1))) -
                               instances_tested * mean_width * mean_entropy) / \
                              math.sqrt((instances_tested * sum(w ** 2 for w in range(5, n_max + 1)) - instances_tested * mean_width ** 2) *
                                        (instances_tested * sum(e ** 2 for e in range(5, n_max + 1)) - instances_tested * mean_entropy ** 2))
    
    conjecture_holds = correlation_coefficient >= 0.9
    counterexample = "" if conjecture_holds else f"correlation_coefficient={correlation_coefficient}"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and min(r["correlation_coefficient"] for r in results) < 0.5:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")