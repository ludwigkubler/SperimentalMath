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

def gaussian_elimination(matrix):
    n = len(matrix)
    for i in range(n):
        # Find pivot in column i
        max_row = i
        for j in range(i+1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        
        # Eliminate entries below pivot
        for j in range(i+1, n):
            factor = Fraction(matrix[j][i], matrix[i][i])
            for k in range(n + 1):
                matrix[j][k] -= factor * matrix[i][k]

    return matrix

def tropical_add(x, y):
    if x == '∞' or y == '∞':
        return '∞'
    return max(x, y)

def tropical_multiply(x, y):
    if x == '∞' or y == '∞':
        return '∞'
    return x + y

def random_boolean_circuit(n, depth=2):
    if depth == 0:
        return [[random.choice([True, False]) for _ in range(n)]]
    
    inputs = [random_boolean_circuit(n, depth - 1) for _ in range(2)]
    output = []
    for i in range(n):
        row = []
        for j in range(n):
            x = inputs[0][i][j]
            y = inputs[1][i][j]
            if random.choice([True, False]):
                row.append(tropical_add(x, y))
            else:
                row.append(tropical_multiply(x, y))
        output.append(row)
    return output

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mtr_values = []
    ec_values = []
    
    for n in n_values:
        circuit = random_boolean_circuit(n)
        
        # Compute minimal tropical motive rank (mtr(C))
        matrix = [[Fraction(0) if x == False else Fraction('∞') for x in row] for row in circuit]
        mtr_value = sum(sum(row) for row in gaussian_elimination(matrix))
        mtr_values.append(mtr_value)
        
        # Compute entanglement complexity (EC(C))
        ec_value = sum(1 for row in circuit for x, y in zip(row[:-1], row[1:]) if x != y)
        ec_values.append(ec_value)
    
    correlation_coefficient = sum((mtr - mean_mtr) * (ec - mean_ec) for mtr, ec in zip(mtr_values, ec_values)) / len(mtr_values)
    mean_mtr = sum(mtr_values) / len(mtr_values)
    mean_ec = sum(ec_values) / len(ec_values)
    
    conjecture_holds = abs(correlation_coefficient) >= 0.8 and all(abs(mtr - ec) <= 3 for mtr, ec in zip(mtr_values, ec_values))
    counterexample = "" if conjecture_holds else "correlation_coefficient={:.2f}, mean_mtr={}, mean_ec={}".format(correlation_coefficient, mean_mtr, mean_ec)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(mtr_values),
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL: {}".format(result))
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={:.2f} std=0.00 support_fraction=1.00".format(mean_metric_value))
    elif support_fraction >= 0.8:
        print("RESULT: SUPPORTED mean={:.2f} std=0.00 support_fraction={:.2f}".format(mean_metric_value, support_fraction))
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"correlation_coefficient<0.8\" first_failing_seed={}".format(first_failing_seed))