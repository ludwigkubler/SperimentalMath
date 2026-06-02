# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 ** n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(abs(x) != abs(y) for x, y in combinations(clause, 2)):
                clauses.append(clause)
        return clauses
    
    def min_order(cnf):
        n = len(cnf[0])
        order = 1
        while True:
            valid = True
            for clause in cnf:
                if any(abs(x) == abs(y) for x, y in combinations(clause, 2)):
                    continue
                if all(abs(coeff) < 1e-6 for coeff in [sum([x**i for x in clause]) for i in range(order)]):
                    valid = False
                    break
            if valid:
                return order
            order += 1
    
    def frege_proof_length(cnf):
        # Simplified DPLL solver to estimate proof length
        stack = []
        assignment = {}
        def dpll():
            if not cnf:
                return True, len(stack)
            literal = next((x for x in range(1, n + 1) if x not in assignment and -x not in assignment), None)
            if literal is None:
                return False, 0
            assignment[literal] = True
            stack.append(literal)
            for clause in cnf:
                if all(x not in assignment or assignment[x] != (x > 0) for x in clause):
                    continue
                if any(-x not in assignment or assignment[-x] != (x < 0) for x in clause):
                    return False, 0
            result, length = dpll()
            if result:
                return True, length
            del assignment[literal]
            stack.pop()
            assignment[-literal] = True
            stack.append(-literal)
            for clause in cnf:
                if all(x not in assignment or assignment[x] != (x > 0) for x in clause):
                    continue
                if any(-x not in assignment or assignment[-x] != (x < 0) for x in clause):
                    return False, 0
            result, length = dpll()
            if result:
                return True, length
            del assignment[-literal]
            stack.pop()
            return False, 0
        return dpll()[1]
    
    n_values = [5, 10, 15, 20, 30, 40]
    min_orders = []
    proof_lengths = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        min_order_value = min_order(cnf)
        proof_length_value = frege_proof_length(cnf)
        min_orders.append(min_order_value)
        proof_lengths.append(proof_length_value)
    
    if len(min_orders) < 30 or len(proof_lengths) < 30:
        return {
            "metric_name": "Pearson correlation coefficient",
            "metric_value": None,
            "instances_tested": len(min_orders),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_min_order = sum(min_orders) / len(min_orders)
    mean_proof_length = sum(proof_lengths) / len(proof_lengths)
    correlation_coefficient = 0.0
    for i in range(len(min_orders)):
        correlation_coefficient += (min_orders[i] - mean_min_order) * (proof_lengths[i] - mean_proof_length)
    correlation_coefficient /= len(min_orders) * math.sqrt(sum((x - mean_min_order)**2 for x in min_orders)) * math.sqrt(sum((y - mean_proof_length)**2 for y in proof_lengths))
    
    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(min_orders),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation_coefficient) > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, min_order={min(r['metric_name'], key=lambda x: len(x))}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break