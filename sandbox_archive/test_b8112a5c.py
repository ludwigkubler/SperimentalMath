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
    
    def generate_random_formula(n):
        if n == 1:
            return random.choice(['0', '1'])
        else:
            subformulas = [generate_random_formula(random.randint(1, n-1)) for _ in range(2)]
            operator = random.choice(['&', '|'])
            return f"({subformulas[0]} {operator} {subformulas[1]})"
    
    def monomial_representation(formula):
        if formula == '0':
            return [0]
        elif formula == '1':
            return [1]
        else:
            left, operator, right = formula.split()
            left_rep = monomial_representation(left)
            right_rep = monomial_representation(right)
            if operator == '&':
                return [x * y for x in left_rep for y in right_rep]
            elif operator == '|':
                return list(set([x for x in left_rep] + [y for y in right_rep]))
    
    def min_local_ring_norm(rep):
        n = len(rep)
        A = [[0] * (n+1) for _ in range(n+1)]
        for i in range(1, n+1):
            A[i][i-1] = 1
            A[i][i] = rep[i-1]
        for k in range(2, n+1):
            pivot_row = max(range(k, n+1), key=lambda r: abs(A[r][k-1]))
            if A[pivot_row][k-1] == 0:
                continue
            A[k-1], A[pivot_row] = A[pivot_row], A[k-1]
            for i in range(n+1):
                A[k-1][i] /= A[k-1][k-1]
            for r in range(n+1):
                if r != k-1:
                    factor = A[r][k-1]
                    for i in range(n+1):
                        A[r][i] -= factor * A[k-1][i]
        return abs(A[n][n])
    
    def resolution_proof_width(formula):
        stack = []
        for char in formula:
            if char == '(':
                stack.append(char)
            elif char == ')':
                count = 0
                while stack[-1] != '(':
                    stack.pop()
                    count += 1
                stack.pop()
                stack.append(count + 1)
            else:
                continue
        return max(stack)

    n_values = [5, 10, 15, 20, 30, 40]
    minLRN_sum = 0
    w_sum = 0
    instances_tested = 0
    n_max = 0

    for n in n_values:
        for _ in range(5):
            formula = generate_random_formula(n)
            rep = monomial_representation(formula)
            minLRN = min_local_ring_norm(rep)
            w = resolution_proof_width(formula)
            if minLRN == 0 or w == 0:
                continue
            minLRN_sum += minLRN
            w_sum += w
            instances_tested += 1
            n_max = max(n_max, n)

    if instances_tested < 30:
        return {
            "metric_name": "minLRN/w",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }

    mean_minLRN = minLRN_sum / instances_tested
    mean_w = w_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(minLRN * w for minLRN, w in zip(monomial_representation(generate_random_formula(n)), resolution_proof_width(generate_random_formula(n)))) - minLRN_sum * w_sum) / math.sqrt((instances_tested * sum(minLRN**2 for minLRN in monomial_representation(generate_random_formula(n))) - minLRN_sum**2) * (instances_tested * sum(w**2 for w in resolution_proof_width(generate_random_formula(n))) - w_sum**2))

    return {
        "metric_name": "minLRN/w",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and 1 <= mean_minLRN / mean_w <= 10,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")