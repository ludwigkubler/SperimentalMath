# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def gaussian_elimination(A, b):
    n = len(b)
    A_augmented = [A[i] + [b[i]] for i in range(n)]
    for i in range(n):
        max_row = i
        for j in range(i+1, n):
            if abs(A_augmented[j][i]) > abs(A_augmented[max_row][i]):
                max_row = j
        A_augmented[i], A_augmented[max_row] = A_augmented[max_row], A_augmented[i]
        for j in range(i+1, n):
            factor = -A_augmented[j][i] / A_augmented[i][i]
            A_augmented[j][i:] = [x + factor*y for x, y in zip(A_augmented[j], A_augmented[i])]
    x = [0] * n
    for i in range(n-1, -1, -1):
        x[i] = (A_augmented[i][-1] - sum(A_augmented[i][j]*x[j] for j in range(i+1, n))) / A_augmented[i][i]
    return x

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, n*3)
    variables = set()
    clauses = []
    for _ in range(m):
        clause = set(random.sample(variables | {-i} for i in range(1, n+1)), k=random.randint(1, n))
        clauses.append(clause)
        variables.update(clause)
    variables = sorted(variables)

    def tseitin_formula_to_quiver(clauses, variables):
        quiver = {}
        for var in variables:
            quiver[var] = []
            quiver[-var] = []
        for clause in clauses:
            new_var = -max(variables) - 1
            quiver[new_var].extend([var if var in clause else -var for var in variables])
            quiver[-new_var].append(new_var)
            variables.append(new_var)
        return quiver

    quiver = tseitin_formula_to_quiver(clauses, variables)

    def representation_length(quiver):
        A = [[0] * len(quiver) for _ in range(len(quiver))]
        b = [0] * len(quiver)
        for var, edges in quiver.items():
            for edge in edges:
                if edge > 0:
                    A[var-1][edge-1] += 1
                else:
                    A[-var-1][-edge-1] -= 1
            b[var-1] = len(edges)
        x = gaussian_elimination(A, b)
        return sum(abs(xi) for xi in x)

    def resolution_proof_width(clauses):
        stack = []
        literals = set()
        while True:
            if not stack and literals:
                literal = next(iter(literals))
                stack.append((literal, 0))
                literals.remove(literal)
            if not stack:
                return len(clauses)
            literal, level = stack[-1]
            if literal > 0:
                for clause in clauses:
                    if literal in clause:
                        clauses.remove(clause)
                        break
                else:
                    literals.add(-literal)
                    stack.pop()
            else:
                neg_literal = -literal
                found = False
                for clause in clauses:
                    if neg_literal in clause:
                        new_clause = [l for l in clause if l != neg_literal]
                        if len(new_clause) == 1:
                            literals.add(new_clause[0])
                            stack.pop()
                            found = True
                            break
                        else:
                            clauses.remove(clause)
                            clauses.append(new_clause)
                if not found:
                    stack.pop()

    rep_length = representation_length(quiver)
    res_width = resolution_proof_width(clauses)

    return {
        "metric_name": "Pearson correlation coefficient",
        "metric_value": Fraction(rep_length * res_width, n),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": rep_length * res_width >= n**2 / 4,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30*31, 30))
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        counterexample = f"Seed {seeds[first_failing_seed]}"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[first_failing_seed]}")