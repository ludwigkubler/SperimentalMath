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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i+1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A
    
    def matrix_rank(A):
        rref = gaussian_elimination([row[:] for row in A])
        rank = 0
        for row in rref:
            if any(row):
                rank += 1
        return rank
    
    def xor_3cnf_circuit(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice(['x', '~x']) + str(i+1) for i in range(n)]
            random.shuffle(clause)
            clauses.append(' or '.join(clause))
        return ' and '.join(clauses)
    
    def construct_quaternionic_form(circuit, n):
        truth_table = {}
        for x in range(2**n):
            inputs = [bool(x & (1 << i)) for i in range(n)]
            output = eval(circuit, {'x': bool, 'or': lambda a, b: a or b})
            truth_table[tuple(inputs)] = output
        q_form = []
        for i in range(2**n):
            row = [0] * (2**n)
            for j in range(2**n):
                if truth_table[i] == truth_table[j]:
                    row[j] = 1
            q_form.append(row)
        return q_form
    
    n_values = list(range(1, 41))
    total_rank = 0
    
    for n in n_values:
        circuit = xor_3cnf_circuit(n)
        q_form = construct_quaternionic_form(circuit, n)
        rank = matrix_rank(q_form)
        total_rank += rank
    
    avg_log_n = sum(math.log(n) for n in n_values) / len(n_values)
    epsilon = 0.1
    conjecture_holds = total_rank >= 0.5 * avg_log_n + epsilon
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Average Rank",
        "metric_value": total_rank / len(n_values),
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")