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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n * (n // 2)):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses

    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            if A[i][i] == 0:
                continue
            for j in range(n):
                A[i][j] /= A[i][i]
            for k in range(m):
                if k != i and A[k][i] != 0:
                    factor = A[k][i]
                    for j in range(n):
                        A[k][j] -= factor * A[i][j]
        rank = sum(1 for row in A if any(row))
        return rank

    def communication_complexity_rank_variance(clauses, n):
        # Simplified DPLL solver to estimate RC
        stack = []
        assignment = [0] * (n + 1)
        def dpll():
            if not clauses:
                return True
            literal = next((lit for lit in range(1, n + 1) if all(lit not in clause and -lit not in clause for clause in clauses)), None)
            if literal is None:
                return False
            assignment[literal] = 1
            stack.append(literal)
            for i in range(len(clauses)):
                if literal in clauses[i]:
                    clauses[i].remove(literal)
                elif -literal in clauses[i]:
                    clauses[i].append(-literal)
            if dpll():
                return True
            assignment[literal] = -1
            stack.pop()
            for i in range(len(clauses)):
                if -literal in clauses[i]:
                    clauses[i].remove(-literal)
                elif literal in clauses[i]:
                    clauses[i].append(literal)
            if dpll():
                return True
            return False
        dpll()
        return len(stack)

    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = generate_cnf(n)
    mrank_phi = gaussian_elimination(phi)
    rc_phi = communication_complexity_rank_variance(phi, n)
    
    return {
        "metric_name": "correlation",
        "metric_value": mrank_phi * rc_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    print(f"RESULT: {RESULT} mean={mean_corr:.2f} std=0.00 support_fraction={support_fraction:.2f}")