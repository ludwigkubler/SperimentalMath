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
    n = random.randint(5, 40)
    s = random.randint(1, 10)
    
    # Generate a random Boolean function f computable by an AC0 parity circuit of size s
    truth_table = [[random.choice([0, 1]) for _ in range(s)] for _ in range(2**s)]
    
    # Construct the algebraic curve using the characteristic polynomial of its truth table
    def characteristic_polynomial(table):
        n = len(table)
        x = [1] + [0] * (n - 1)
        for row in table:
            new_x = [1]
            for i in range(n):
                new_x.append((new_x[-1] + row[i]) % 2)
            x = new_x
        return x
    
    poly = characteristic_polynomial(truth_table)
    
    # Calculate the rank of the variety defined by the curve's defining equations
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        for i in range(m):
            if matrix[i][i] == 0:
                for j in range(i + 1, m):
                    if matrix[j][i] != 0:
                        matrix[i], matrix[j] = matrix[j], matrix[i]
                        break
                    else:
                        continue
                else:
                    return i - 1
            for j in range(n):
                if j == i:
                    continue
                factor = matrix[j][i] / matrix[i][i]
                for k in range(m):
                    matrix[j][k] -= factor * matrix[i][k]
        return m
    
    rank = matrix_rank(poly)
    
    # Measure the correlation between R(f) and s
    g = math.ceil(math.sqrt(2 * rank))
    expected_slope = (g**2 / s)
    observed_slope = (rank / s)
    
    metric_name = "Slope"
    metric_value = observed_slope
    instances_tested = 1
    conjecture_holds = abs(observed_slope - expected_slope) <= 0.1 * expected_slope
    counterexample = "" if conjecture_holds else f"Observed slope {observed_slope}, Expected slope {expected_slope}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")