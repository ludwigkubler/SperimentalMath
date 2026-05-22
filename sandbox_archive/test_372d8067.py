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

def gaussian_elimination(A):
    m, n = len(A), len(A[0])
    for i in range(m):
        max_row = i + max(range(i, m), key=lambda k: abs(A[k][i]))
        A[i], A[max_row] = A[max_row], A[i]
        for j in range(n):
            if j != i:
                factor = Fraction(A[j][i], A[i][i])
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def rank_of_matrix(A):
    A = gaussian_elimination(A)
    rank = sum(1 for row in A if any(row))
    return rank

def gram_matrix(CNF_formula):
    n = len(CNF_formula)
    G = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in CNF_formula:
        for literal in clause:
            i = abs(literal) - 1
            if literal > 0:
                G[i][n] += 1
                G[n][i] += 1
            else:
                G[0][i] -= 1
                G[i][0] -= 1
    return G

def resolution_proof_length(CNF_formula):
    n = len(CNF_formula)
    proof = []
    while True:
        new_clauses = set()
        for i in range(n):
            for j in range(i + 1, n):
                if any(l not in clause and -l not in clause for l in CNF_formula[i] + CNF_formula[j]):
                    new_clause = list(set(CNF_formula[i]) | set(CNF_formula[j]))
                    new_clauses.add(tuple(sorted(new_clause)))
        if not new_clauses:
            break
        proof.extend(new_clauses)
        CNF_formula.extend(new_clauses)
    return len(proof)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    CNF_formula = []
    for _ in range(n):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
        CNF_formula.append(tuple(sorted(clause)))
    
    G = gram_matrix(CNF_formula)
    rank = rank_of_matrix(G)
    proof_length = resolution_proof_length(CNF_formula)
    
    if proof_length == 0:
        return {
            "metric_name": "Ratio of Rank to Proof Length",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Empty resolution proof"
        }
    
    ratio = rank / proof_length
    return {
        "metric_name": "Ratio of Rank to Proof Length",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio <= 10 ** (1/2),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds threshold\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE Reason=All trials used n=1")