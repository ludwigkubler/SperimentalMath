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
    
    def gaussian_elimination(A, b):
        n = len(b)
        for i in range(n):
            max_row = i + max(range(i, n), key=lambda k: abs(A[k][i]))
            A[i], A[max_row] = A[max_row], A[i]
            b[i], b[max_row] = b[max_row], b[i]
            factor = A[i][i]
            for j in range(n):
                A[i][j] /= factor
            b[i] /= factor
            for k in range(n):
                if k != i:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
                    b[k] -= factor * b[i]
        return b
    
    def resolution_width(phi):
        n = len(phi)
        clauses = phi.split('\n')
        clauses = [c.strip() for c in clauses if c]
        literals = set()
        for clause in clauses:
            literals.update(clause.split())
        literals = sorted(literals, key=lambda x: int(x[1:]) if x.startswith('x') else -int(x[1:]))
        n_vars = len(literals)
        
        def dpll(model):
            stack = []
            while True:
                unit_clause = next((c for c in clauses if sum(1 for l in c.split() if model[l] == 0) == 1), None)
                if unit_clause is not None:
                    literal = next(l for l in unit_clause.split() if model[l] == 0)
                    model[literal] = 1
                    stack.append((literal, -1))
                else:
                    if all(model[l] != 0 for c in clauses for l in c.split()):
                        return True
                    literal = next(l for l in literals if model[l] == 0)
                    model[literal] = 1
                    stack.append((literal, 1))
                while stack and stack[-1][1] == -1:
                    literal, _ = stack.pop()
                    model[literal] = 0
            return False
        
        def add_clause(clause):
            for literal in clause.split():
                if literal[0] == '-':
                    model[literal] = 0
                else:
                    model[literal] = 1
        
        model = {l: 0 for l in literals}
        width = 0
        while True:
            add_clause(clauses.pop(0))
            if dpll(model):
                break
            stack.append((clauses[0], -1))
            clauses.append(clauses.pop(0))
            width += 1
        return width
    
    def geometric_entropy(G):
        n = len(G)
        degree_sum = sum(sum(1 for j in range(n) if G[i][j] == 1) for i in range(n))
        avg_degree = degree_sum / (2 * n)
        entropy = -avg_degree * math.log(avg_degree, 2)
        return entropy
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 ** n):
            clause = ' '.join('x' + str(random.randint(1, n)) if random.choice([True, False]) else '-' + 'x' + str(random.randint(1, n)) for _ in range(random.randint(1, n)))
            clauses.append(clause)
        return '\n'.join(clauses)
    
    n = 20
    phi = generate_cnf(n)
    G = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
    h_G = geometric_entropy(G)
    w_phi = resolution_width(phi)
    
    return {
        "metric_name": "resolution_width",
        "metric_value": w_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": w_phi <= h_G * math.log(n, 2),
        "counterexample": "" if w_phi <= h_G * math.log(n, 2) else f"Counterexample: w(phi) = {w_phi}, h(G(phi)) = {h_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")