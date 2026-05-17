# auto-injected by SEC sandbox
import collections
import json
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import sys
import random
import math
import itertools
from fractions import Fraction

def generate_3cnf(n, alpha, seed):
    random.seed(seed)
    m = int(alpha * n)
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause_vars = random.sample(variables, 3)
        clause = []
        for var in clause_vars:
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(-var)
        clauses.append(clause)
    return clauses

def generate_tseitin(n, seed):
    random.seed(seed)
    edges = list(itertools.combinations(range(1, n + 1), 2))
    random.shuffle(edges)
    m = n
    clauses = []
    for i in range(m):
        u, v = edges[i]
        w = n + i + 1
        clauses.append([u, v, -w])
        clauses.append([u, -v, w])
        clauses.append([-u, v, w])
        clauses.append([-u, -v, -w])
    return clauses

def is_satisfiable(clauses, n):
    def backtrack(assignment, clause_index):
        if clause_index == len(clauses):
            return True
        clause = clauses[clause_index]
        for lit in clause:
            var = abs(lit)
            if var in assignment:
                if (lit > 0 and assignment[var]) or (lit < 0 and not assignment[var]):
                    if backtrack(assignment, clause_index + 1):
                        return True
            else:
                assignment[var] = lit > 0
                if backtrack(assignment, clause_index + 1):
                    return True
                del assignment[var]
                assignment[var] = lit < 0
                if backtrack(assignment, clause_index + 1):
                    return True
                del assignment[var]
        return False

    return backtrack({}, 0)

def compute_mu_H(F, n):
    def lit(l, x):
        if l > 0:
            return x[l - 1]
        else:
            return 1 - x[-l - 1]

    def compute_H(F, n):
        H = [[0 for _ in range(n)] for _ in range(n)]
        for clause in F:
            l1, l2, l3 = clause
            for a in range(n):
                for b in range(n):
                    if a == b:
                        continue
                    term = lit(l1, [1 if i == a or i == b else 0 for i in range(n)]) * lit(l2, [1 if i == a or i == b else 0 for i in range(n)])
                    term *= lit(l3, [1 if i == a or i == b else 0 for i in range(n)])
                    H[a][b] += term
        return H

    def matrix_rank(M):
        n = len(M)
        rank = 0
        for i in range(n):
            if i >= len(M) or i >= len(M[0]):
                break
            pivot = i
            while pivot < n and M[pivot][i] == 0:
                pivot += 1
            if pivot == n:
                continue
            M[i], M[pivot] = M[pivot], M[i]
            rank += 1
            for j in range(i + 1, n):
                if M[j][i] != 0:
                    factor = Fraction(M[j][i], M[i][i]) if M[i][i] != 0 else 0
                    for k in range(i, n):
                        M[j][k] -= factor * M[i][k]
        return rank

    u = [random.random() for _ in range(n)]
    H = compute_H(F, n)
    H_u = [[sum(H[i][j] * u[k] for k in range(n)) for j in range(n)] for i in range(n)]
    r_F = matrix_rank(H_u)
    mu_H = math.floor(math.log2(1 + r_F))
    return mu_H

def compute_resolution_width(F, n):
    def is_tautology(clause):
        for lit in clause:
            if -lit in clause:
                return True
        return False

    def resolve(c1, c2):
        resolved = []
        for lit in c1:
            if -lit not in c2:
                resolved.append(lit)
        for lit in c2:
            if -lit not in c1:
                resolved.append(lit)
        return resolved

    def derive_clauses(clauses, width):
        derived = set(tuple(sorted(clause)) for clause in clauses)
        for _ in range(width):
            new_clauses = set()
            for c1, c2 in itertools.combinations(derived, 2):
                if len(c1) + len(c2) - len(set(c1) & set(c2)) <= width:
                    resolved = resolve(c1, c2)
                    if not is_tautology(resolved):
                        new_clauses.add(tuple(sorted(resolved)))
            if not new_clauses:
                break
            derived.update(new_clauses)
        return derived

    for w in range(1, 9):
        derived = derive_clauses(F, w)
        if any(len(clause) == 0 for clause in derived):
            return w
    return float('inf')

def run_trial(seed):
    n_values = [10, 15, 20, 25, 30, 35, 40]
    alpha_values = [5, 6, 8]
    instances_tested = 0
    metric_values = []
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        for alpha in alpha_values:
            for _ in range(5):
                F = generate_3cnf(n, alpha, seed)
                if not is_satisfiable(F, n):
                    instances_tested += 1
                    mu_H = compute_mu_H(F, n)
                    w_star = compute_resolution_width(F, n)
                    metric_values.append(mu_H)
                    if mu_H > w_star:
                        conjecture_holds = False
                        counterexample = f"mu_H(F) = {mu_H} > w*(F) = {w_star} for n={n}, alpha={alpha}"
                        break
                if not conjecture_holds:
                    break
            if not conjecture_holds:
                break
            for _ in range(5):
                F = generate_tseitin(n, seed)
                if not is_satisfiable(F, n):
                    instances_tested += 1
                    mu_H = compute_mu_H(F, n)
                    w_star = compute_resolution_width(F, n)
                    metric_values.append(mu_H)
                    if mu_H > w_star:
                        conjecture_holds = False
                        counterexample = f"mu_H(F) = {mu_H} > w*(F) = {w_star} for n={n}, Tseitin"
                        break
                if not conjecture_holds:
                    break
            if not conjecture_holds:
                break
        if not conjecture_holds:
            break

    if instances_tested == 0:
        return {
            "metric_name": "mu_H(F)",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No unsatisfiable instances generated"
        }

    mean_metric = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "mu_H(F)",
        "metric_value": mean_metric,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    metric_values = [r["metric_value"] for r in results if r["instances_tested"] > 0]
    if not metric_values:
        print("RESULT: INCONCLUSIVE reason=no_unsat_instances")
        sys.exit(0)

    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")