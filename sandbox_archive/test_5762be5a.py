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
    
    def generate_circuit(n):
        # Generate a random Boolean circuit with n variables
        if n == 1:
            return ['0']
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return [f'({l} AND {r})' for l in left] + [f'({l} OR {r})' for l in right]
    
    def construct_noncommutative_algebra(circuit):
        # Construct the noncommutative algebra N for the circuit
        variables = set()
        generators = []
        relations = []
        
        def parse_expression(expr):
            if expr.startswith('(') and expr.endswith(')'):
                expr = expr[1:-1]
            if ' AND ' in expr:
                left, right = expr.split(' AND ')
                return parse_expression(left), parse_expression(right)
            elif ' OR ' in expr:
                left, right = expr.split(' OR ')
                return parse_expression(left), parse_expression(right)
            else:
                variables.add(expr)
                return expr
        
        def add_relation(g1, g2):
            if (g1, g2) not in relations and (g2, g1) not in relations:
                relations.append((g1, g2))
        
        for expr in circuit:
            left, right = parse_expression(expr)
            if isinstance(left, tuple):
                add_relation(left[0], right[0])
                add_relation(left[1], right[1])
            else:
                add_relation(left, right)
        
        return variables, generators, relations
    
    def compute_minimal_rank(variables, generators, relations):
        # Calculate the minimal rank ρ(C) of the algebra N
        n = len(variables)
        m = len(relations)
        if m == 0:
            return 1
        
        # Gaussian elimination to find the rank
        A = [[Fraction(0, 1)] * (n + m) for _ in range(n + m)]
        for i, var in enumerate(variables):
            A[i][i] = Fraction(1, 1)
        
        for j, rel in enumerate(relations):
            g1, g2 = rel
            if g1 in variables:
                idx1 = variables.index(g1)
                for k in range(n + m):
                    A[idx1][k] += A[j][k]
            if g2 in variables:
                idx2 = variables.index(g2)
                for k in range(n + m):
                    A[idx2][k] += A[j][k]
        
        rank = 0
        for row in A[:n]:
            if any(x != Fraction(0, 1) for x in row):
                rank += 1
        
        return rank
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    variables, generators, relations = construct_noncommutative_algebra(circuit)
    rho_C = compute_minimal_rank(variables, generators, relations)
    
    conjecture_holds = rho_C <= n * math.log2(n)
    counterexample = "" if conjecture_holds else f"rho(C)={rho_C}, expected O({n} log {n})"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rho_C,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho_C = sum(r["metric_value"] for r in results) / len(results)
    std_rho_C = math.sqrt(sum((r["metric_value"] - mean_rho_C)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho_C} std={std_rho_C} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.95:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")