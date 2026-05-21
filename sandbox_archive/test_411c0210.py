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

    def matrix_multiplication(A, B):
        m, n, p = len(A), len(B), len(B[0])
        C = [[0]*p for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    C[i][j] += A[i][k] * B[k][j]
        return C

    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit = None
        for clause in clauses:
            if len(clause) == 1:
                unit = clause[0]
                break
        if unit is not None:
            new_assignment = assignment.copy()
            new_assignment[unit] = True
            if dpll([c for c in clauses if unit not in c and -unit not in c], new_assignment):
                return True
            new_assignment[unit] = False
            if dpll([c for c in clauses if unit not in c and -unit not in c], new_assignment):
                return True
        else:
            literal = random.choice(clauses[0])
            new_assignment = assignment.copy()
            new_assignment[literal] = True
            if dpll(clauses, new_assignment):
                return True
            new_assignment[literal] = False
            if dpll(clauses, new_assignment):
                return True
        return False

    def tseitin_formula(n):
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([-i, -j, -(n+i+j)])
                clauses.append([i, j, n+i+j])
        return clauses

    def clique_complex(n):
        G = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if random.choice([True, False]):
                    G[i][j] = 1
                    G[j][i] = 1
        return G

    def persistent_homology(G):
        n = len(G)
        simplices = []
        for i in range(n):
            simplices.append([i])
        for k in range(2, n+1):
            new_simps = []
            for s in simplices:
                for j in range(k-1):
                    if s[j] not in G[s[-1]]:
                        break
                else:
                    new_simps.append(s + [k-1])
            simplices.extend(new_simps)
        barcode = {}
        for s in simplices:
            birth = math.inf
            death = -math.inf
            for i in range(len(s)-1):
                if G[s[i]][s[i+1]]:
                    birth = min(birth, max([G[s[j]][s[k]] for j in range(i) for k in range(i+2, len(s))]))
                    death = max(death, min([G[s[j]][s[k]] for j in range(i+1) for k in range(i+2, len(s))]))
            if birth < math.inf and death > -math.inf:
                barcode[birth] = death
        return barcode

    def resolution_length(clauses):
        assignment = {}
        return dpll(clauses, assignment)

    n = random.randint(5, 40)
    G = clique_complex(n)
    barcode = persistent_homology(G)
    nu_G = max(barcode.values()) if barcode else 1
    clauses = tseitin_formula(n)
    resolution_len = resolution_length(clauses)
    
    return {
        "metric_name": "resolution_length",
        "metric_value": resolution_len,
        "instances_tested": 1,
        "conjecture_holds": resolution_len >= 2**(0.2 * nu_G),
        "counterexample": "" if resolution_len >= 2**(0.2 * nu_G) else f"Graph with n={n}, barcode_length={nu_G}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Graph with n={results[0]['instances_tested']}, barcode_length={results[0]['metric_value']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")