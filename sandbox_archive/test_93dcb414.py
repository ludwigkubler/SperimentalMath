# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(random.randint(2, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                clauses.append(clause)
        return clauses
    
    def vector_space_from_cnf(cnf):
        n = len(cnf)
        V = [[0] * (2**n) for _ in range(n)]
        for i, clause in enumerate(cnf):
            mask = 0
            for lit in clause:
                if lit > 0:
                    mask |= 1 << (lit - 1)
                else:
                    mask &= ~(1 << (-lit - 1))
            V[i] = [mask & (1 << j) != 0 for j in range(2**n)]
        return V
    
    def linear_operators(V):
        n, m = len(V), len(V[0])
        ops = []
        for i in range(n):
            for j in range(m):
                if V[i][j]:
                    op = [[0] * m for _ in range(m)]
                    for k in range(m):
                        if V[i][k]:
                            op[j][k] = 1
                    ops.append(op)
        return ops
    
    def minimal_index_of_coadjointness(ops):
        n, m = len(ops), len(ops[0])
        indices = [0] * n
        for i in range(n):
            for j in range(m):
                if ops[i][j]:
                    indices[i] += 1
        return min(indices)
    
    def resolution_width(cnf):
        stack = []
        seen = set()
        for clause in cnf:
            stack.append(clause)
            seen.update(clause)
        
        while stack:
            clause = stack.pop()
            if not clause:
                return len(seen)
            lit = next(lit for lit in clause if lit > 0 and -lit not in seen)
            seen.add(-lit)
            new_clauses = []
            for other_clause in cnf:
                if any(abs(l) == abs(lit) for l in other_clause):
                    continue
                new_clause = [l for l in other_clause if l != -lit]
                if not new_clause:
                    return len(seen)
                new_clauses.append(new_clause)
            stack.extend(new_clauses)
        
        return len(seen)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        V = vector_space_from_cnf(cnf)
        ops = linear_operators(V)
        index = minimal_index_of_coadjointness(ops)
        width = resolution_width(cnf)
        results.append((index, width))
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    indices, widths = zip(*results)
    mean_index = sum(indices) / len(indices)
    mean_width = sum(widths) / len(widths)
    correlation_coefficient = (sum((indices[i] - mean_index) * (widths[i] - mean_width) for i in range(len(indices))) /
                               (len(indices) * sum((indices[i] - mean_index)**2 for i in range(len(indices)))**0.5 *
                                sum((widths[i] - mean_width)**2 for i in range(len(widths)))**0.5))
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")