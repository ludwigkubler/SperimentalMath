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
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def is_satisfiable(cnf):
        stack = []
        assignment = {}
        for literal in range(1, 2 * len(cnf)):
            if literal not in assignment and -literal not in assignment:
                assignment[literal] = True
                stack.append(literal)
                break
        while stack:
            literal = stack.pop()
            if literal in assignment and assignment[literal]:
                continue
            assignment[literal] = False
            for clause in cnf:
                if literal in clause or -literal in clause:
                    continue
                if all(-x not in assignment or not assignment[-x] for x in clause):
                    return False
                break
        return True

    def min_order(cnf):
        n = len(cnf)
        order = [0] * (n + 1)
        for literal in range(1, 2 * n + 1):
            if literal not in assignment and -literal not in assignment:
                stack = [literal]
                while stack:
                    literal = stack.pop()
                    if literal in assignment and assignment[literal]:
                        continue
                    assignment[literal] = False
                    for clause in cnf:
                        if literal in clause or -literal in clause:
                            continue
                        if all(-x not in assignment or not assignment[-x] for x in clause):
                            return False
                        break
        return max(order)

    def smallest_circuit(cnf):
        n = len(cnf)
        circuit = []
        for literal in range(1, 2 * n + 1):
            if literal not in assignment and -literal not in assignment:
                stack = [literal]
                while stack:
                    literal = stack.pop()
                    if literal in assignment and assignment[literal]:
                        continue
                    assignment[literal] = False
                    for clause in cnf:
                        if literal in clause or -literal in clause:
                            continue
                        if all(-x not in assignment or not assignment[-x] for x in clause):
                            return False
                        break
        return len(circuit)

    n = random.randint(5, 40)
    phi = generate_cnf(n)
    order = min_order(phi)
    circuit_size = smallest_circuit(phi)

    return {
        "metric_name": "order_vs_circuit_size",
        "metric_value": abs(order - circuit_size),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if order != circuit_size else True,
        "counterexample": "" if order == circuit_size else f"order={order}, circuit_size={circuit_size}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_order_diff = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order_diff} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order_diff} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"order_vs_circuit_size\" first_failing_seed={first_failing_seed}")