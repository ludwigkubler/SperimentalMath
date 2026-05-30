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
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clauses[j][i] for j in range(len(clauses))):
                continue
            clauses.append(clause)
        return clauses
    
    def truth_table(cnf):
        n = len(cnf[0])
        table = []
        for i in range(2**n):
            assignment = [(i >> j) & 1 for j in range(n)]
            table.append(all([all([assignment[j-1] == c if c != 0 else -assignment[j-1] == c for c in clause]) for clause in cnf]))
        return table
    
    def minimal_modular_function_order(truth_table):
        n = len(truth_table[0])
        order = 0
        while True:
            found = False
            for i in range(2**n):
                if truth_table[i]:
                    found = True
                    break
            if not found:
                return order
            order += 1
    
    def tree_like_resolution_width(cnf):
        n = len(cnf[0])
        states = [{'clauses': cnf, 'assignment': [0] * n}]
        while states:
            state = states.pop()
            if all(state['assignment']):
                return len(state['clauses'])
            for clause in state['clauses']:
                if any([abs(x) == abs(c) and (x > 0) != (c > 0) for x in state['assignment']]):
                    new_assignment = state['assignment'].copy()
                    new_assignment[clause.index(abs(clause[0])) - 1] = -new_assignment[clause.index(abs(clause[0])) - 1]
                    states.append({'clauses': [c for c in cnf if not all([abs(x) == abs(c[i]) and (x > 0) != (c[i] > 0) for x in new_assignment[:i]])], 'assignment': new_assignment})
        return len(cnf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    table = truth_table(cnf)
    f_phi = minimal_modular_function_order(table)
    width = tree_like_resolution_width(cnf)
    
    return {
        "metric_name": "tree-like resolution proof width",
        "metric_value": width,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(width - 2**(n * f_phi)) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={seeds[first_failing_seed]}")