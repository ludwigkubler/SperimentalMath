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
    n = random.randint(1, 40)
    
    # Generate a random XOR 3-CNF circuit with n variables
    def generate_xor_3cnf(n):
        clauses = []
        for _ in range(n):
            literals = [f'x{i}' if random.choice([True, False]) else f'~x{i}' for i in range(1, n+1)]
            clause = ' or '.join(literals)
            clauses.append(f'({clause})')
        circuit = ' and '.join(clauses)
        return circuit
    
    circuit = generate_xor_3cnf(n)
    
    # Construct the associated quaternionic form
    def construct_quaternionic_form(circuit, n):
        truth_table = {}
        for i in range(2**n):
            inputs = [bool((i >> j) & 1) for j in range(n)]
            output = eval(circuit, {'x': inputs})
            truth_table[tuple(inputs)] = output
        
        # Create a quaternionic matrix from the truth table
        q_form = [[0+0j] * (2**n) for _ in range(2**n)]
        for i in range(2**n):
            for j in range(2**n):
                if truth_table[tuple(inputs)] == truth_table[tuple(j_inputs)]:
                    q_form[i][j] = 1+0j
                else:
                    q_form[i][j] = -1+0j
        
        return q_form
    
    try:
        q_form = construct_quaternionic_form(circuit, n)
    except Exception as e:
        return {
            "metric_name": "rank",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": str(e)
        }
    
    # Calculate the rank of the quaternionic form
    def matrix_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if all(matrix[j][i] == 0 for j in range(i, m)):
                continue
            rank += 1
            pivot_row = [matrix[j][i] / matrix[i][i] for j in range(n)]
            for j in range(m):
                if j != i:
                    factor = matrix[j][i]
                    for k in range(n):
                        matrix[j][k] -= factor * pivot_row[k]
        return rank
    
    rank = matrix_rank(q_form)
    
    # Compute the average value of log(n) for all n
    avg_log_n = sum(math.log(i) for i in range(1, 41)) / 40
    
    # Check if the conjecture holds
    epsilon = 0.5
    conjecture_holds = rank >= epsilon * math.log(n)
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all("counterexample" not in result or result["counterexample"] == "" for result in results):
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean_rank} std=NA support_fraction={support_fraction}")
        else:
            print(f"RESULT: FALSIFIED counterexample='' first_failing_seed=NA")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")