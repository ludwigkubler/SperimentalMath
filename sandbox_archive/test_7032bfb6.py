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
    
    def tseitin_formula(n):
        clauses = []
        for i in range(1, n+1):
            clauses.append([i])
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([-i, -j, -(n+i+j)])
                clauses.append([i, j, n+i+j])
        return clauses

    def hamiltonian(clauses):
        n = len(clauses)
        H = [[0] * (2*n) for _ in range(2*n)]
        for clause in clauses:
            for lit in clause:
                if lit > 0:
                    H[lit-1][lit+n-1] += 1
                    H[lit+n-1][lit-1] += 1
                else:
                    H[-lit-1][-lit+n-1] -= 1
                    H[-lit+n-1][-lit-1] -= 1
        return H

    def geometric_entropy(H):
        n = len(H)
        det = determinant(H)
        if det == 0:
            return float('inf')
        return -math.log(abs(det))

    def determinant(matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        det = 0
        for j in range(n):
            submatrix = [row[:j] + row[j+1:] for row in matrix[1:]]
            det += ((-1)**j) * matrix[0][j] * determinant(submatrix)
        return det

    def frege_proof_width(clauses):
        n = len(clauses)
        width = 0
        for clause in clauses:
            width = max(width, len(clause))
        return width

    def run_experiment(n):
        clauses = tseitin_formula(n)
        H = hamiltonian(clauses)
        mge = geometric_entropy(H)
        w = frege_proof_width(clauses)
        return {"metric_name": "mge", "metric_value": mge, "instances_tested": 1, "n_max": n, "conjecture_holds": mge <= 10 * w, "counterexample": ""}

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        result = run_experiment(n)
        results.append(result)

    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "mge",
        "metric_value": total_metric_value / len(results),
        "instances_tested": len(results),
        "n_max": max(r["n_max"] for r in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else "support_fraction < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 39) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_metric_value = sum(r["metric_value"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={total_metric_value/len(results)} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} < 0.8")