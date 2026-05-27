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
    n = random.randint(5, 40)
    D = math.ceil(math.log2(n))
    p = random.choice([2, 3, 5, 7, 11])
    
    # Generate a random Boolean formula with depth D
    def generate_formula(depth):
        if depth == 0:
            return random.choice(['0', '1'])
        else:
            op = random.choice(['&', '|'])
            left = generate_formula(depth - 1)
            right = generate_formula(depth - 1)
            return f'({left} {op} {right})'
    
    formula = generate_formula(D)
    
    # Compute the truth table
    def evaluate(formula, assignment):
        if formula == '0':
            return False
        elif formula == '1':
            return True
        else:
            op, left, right = formula[1:-1].split()
            if op == '&':
                return evaluate(left, assignment) and evaluate(right, assignment)
            elif op == '|':
                return evaluate(left, assignment) or evaluate(right, assignment)
    
    truth_table = []
    for i in range(2**n):
        assignment = [(i >> j) & 1 for j in range(n)]
        truth_table.append(evaluate(formula, assignment))
    
    # Compute the minimal order of the p-adic Galois representation
    def min_order(truth_table, p):
        orders = [0] * len(truth_table)
        for i in range(len(truth_table)):
            if truth_table[i]:
                orders[i] = 1
            else:
                orders[i] = -1
        order = 1
        while True:
            valid = True
            for i in range(len(orders)):
                if orders[i] != 0 and (order * orders[i]) % p == 0:
                    valid = False
                    break
            if valid:
                return order
            order += 1
    
    min_order_val = min_order(truth_table, p)
    
    # Check the conjecture
    if min_order_val < p**D:
        return {
            "metric_name": "min_order",
            "metric_value": min_order_val,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Formula: {formula}, Depth: {D}, Minimal Order: {min_order_val}"
        }
    else:
        return {
            "metric_name": "min_order",
            "metric_value": min_order_val,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        random.seed(seed)
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r for r in results if not r["conjecture_holds"])["seed"]
        print(f"RESULT: FALSIFIED counterexample=\"Formula exceeds p^D\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support")