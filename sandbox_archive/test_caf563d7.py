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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i
            for j in range(i+1, n):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i+1, n):
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(n-1, -1, -1):
            x[i] = Fraction(b[i], A[i][i])
            for j in range(i-1, -1, -1):
                b[j] -= A[j][i] * x[i]
        return x
    
    def is_sat(phi_G):
        stack = []
        for clause in phi_G:
            literals = [l for l in clause if l > 0]
            negated_literals = [-l for l in clause if l < 0]
            if not literals and any(l in stack for l in negated_literals):
                return False
            for literal in literals:
                if -literal in stack:
                    stack.remove(-literal)
                else:
                    stack.append(literal)
        return True
    
    def tseitin_formula(n):
        phi_G = []
        for i in range(1, n+1):
            clause = [i]
            for j in range(i+1, n+1):
                clause.extend([-i, -j, i+j])
            phi_G.append(clause)
        return phi_G
    
    def minimal_generators(phi_G):
        n = len(phi_G)
        A = [[0] * (n+1) for _ in range(n+1)]
        b = [0] * (n+1)
        for clause in phi_G:
            for literal in clause:
                if literal > 0:
                    A[literal][literal] += 1
                    b[literal] += 1
                else:
                    A[-literal][-literal] += 1
                    b[-literal] -= 1
        x = gaussian_elimination(A, b)
        return sum(x[i] != 0 for i in range(1, n+1))
    
    def resolution_width(phi_G):
        stack = []
        width = 0
        while stack:
            clause = stack.pop()
            literals = [l for l in clause if l > 0]
            negated_literals = [-l for l in clause if l < 0]
            if not literals and any(l in stack for l in negated_literals):
                return width
            for literal in literals:
                if -literal in stack:
                    stack.remove(-literal)
                else:
                    stack.append(literal)
            width = max(width, len(stack))
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        phi_G = tseitin_formula(n)
        gen_count = minimal_generators(phi_G)
        proof_width = resolution_width(phi_G)
        results.append((n, gen_count, proof_width))
    
    if any(gen_count < n/2 or proof_width > 10*n**2 for _, gen_count, proof_width in results):
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "generator count < n/2 or proof width > 10n^2"
        }
    
    correlation_coefficient = sum((gen_count - n_values[i]/2) * (proof_width - 5*n_values[i]**2) for i, (n, gen_count, proof_width) in enumerate(results)) / sum((gen_count - n_values[i]/2)**2 for _, gen_count, _ in results)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{trial_result['metric_name']}\", \"metric_value\": {trial_result['metric_value']}, \"instances_tested\": {trial_result['instances_tested']}, \"n_max\": {trial_result['n_max']}, \"conjecture_holds\": {trial_result['conjecture_holds']}, \"counterexample\": \"{trial_result['counterexample']}\"}}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"generator count < n/2 or proof width > 10n^2\" first_failing_seed={first_failing_seed}")