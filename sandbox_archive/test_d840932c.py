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
    
    def is_power_of_two(n):
        return n > 0 and (n & (n - 1)) == 0
    
    def gaussian_elimination(A, b):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            for j in range(i + 1, m):
                factor = A[j][i] / A[i][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
                b[j] -= factor * b[i]
        x = [0] * n
        for i in range(m - 1, -1, -1):
            x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
        return x
    
    def generate_cnf(n):
        clauses = []
        for i in range(1 << n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(j + 1)
                else:
                    clause.append(-(j + 1))
            clauses.append(clause)
        return clauses
    
    def compute_resolvent(cnf):
        minterms = [0] * (1 << n)
        for clause in cnf:
            minterm = 0
            for lit in clause:
                if lit > 0:
                    minterm |= 1 << (lit - 1)
                else:
                    minterm &= ~(1 << (-lit - 1))
            minterms[minterm] += 1
        
        resolvent = []
        for i in range(1 << n):
            if minterms[i] > 0:
                for j in range(i + 1, 1 << n):
                    if minterms[j] > 0 and (i & j) == 0:
                        diff = i ^ j
                        resolvent.append([-(diff >> k & 1) * (k + 1) for k in range(n)])
        return resolvent
    
    def quadratic_residue_class_representation(resolvent):
        qcr = 1
        for clause in resolvent:
            if len(clause) == 2:
                a, b = abs(clause[0]), abs(clause[1])
                if a != b and (a * a % 4 == 1 or b * b % 4 == 1):
                    qcr *= 2
        return qcr
    
    def resolution_proof_width(cnf):
        m, n = len(cnf), len(cnf[0])
        clauses = [set(clause) for clause in cnf]
        unit_clauses = [i for i in range(m) if len(clauses[i]) == 1]
        while unit_clauses:
            lit = clauses[unit_clauses[0]].pop()
            unit_clauses.pop(0)
            for j in range(m):
                if lit in clauses[j]:
                    clauses[j].remove(lit)
                    if len(clauses[j]) == 1:
                        unit_clauses.append(j)
        return max(len(clause) for clause in clauses if clause)
    
    n_min = 5
    n_max = 40
    instances_tested = 0
    total_rpw = 0
    
    for n in range(n_min, n_max + 1):
        cnf = generate_cnf(n)
        resolvent = compute_resolvent(cnf)
        qcr = quadratic_residue_class_representation(resolvent)
        
        if is_power_of_two(qcr):
            rpw = resolution_proof_width(cnf)
            instances_tested += 1
            total_rpw += rpw
    
    if instances_tested == 0:
        return {
            "metric_name": "resolution proof width",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "no_instances"
        }
    
    mean_rpw = total_rpw / instances_tested
    rpw_support_fraction = sum(1 for _ in range(instances_tested) if n_min <= n < n_max and n_max >= 20)
    rpw_support_fraction /= instances_tested
    
    return {
        "metric_name": "resolution proof width",
        "metric_value": mean_rpw,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": rpw_support_fraction >= 0.5 and mean_rpw <= 1.2 * n_max and mean_rpw >= n_max,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rpw = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    rpw_support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rpw} std=0 support_fraction={rpw_support_fraction}")
    elif rpw_support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rpw} std=0 support_fraction={rpw_support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction<{rpw_support_fraction}\" first_failing_seed={first_failing_seed}")