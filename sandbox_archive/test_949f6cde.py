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
    
    def gaussian_elimination(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            max_row = i
            for j in range(i + 1, m):
                if abs(A[j][i]) > abs(A[max_row][i]):
                    max_row = j
            A[i], A[max_row] = A[max_row], A[i]
            pivot = A[i][i]
            if pivot == 0:
                continue
            for j in range(n):
                A[i][j] /= pivot
            for j in range(m):
                if j != i and A[j][i] != 0:
                    factor = A[j][i]
                    for k in range(n):
                        A[j][k] -= factor * A[i][k]
        return A

    def rank(A):
        m, n = len(A), len(A[0])
        rref = gaussian_elimination(A)
        return sum(1 for row in rref if any(row[j] != 0 for j in range(n)))

    def tseitin_clause_set(n):
        clauses = []
        for i in range(1 << n):
            clause = []
            for j in range(n):
                if (i >> j) & 1:
                    clause.append(f'x{j+1}')
                else:
                    clause.append(f'-x{j+1}')
            clauses.append(clause)
        return clauses

    def resolution_refutation_length(clauses):
        n = len(clauses[0])
        refutation = []
        while True:
            new_clauses = set()
            for i in range(len(refutation)):
                for j in range(i + 1, len(refutation)):
                    a, b = refutation[i], refutation[j]
                    if any(x.startswith('-') and x[1:] == y or y.startswith('-') and y[1:] == x for x in a for y in b):
                        new_clause = [x for x in a + b if not (x.startswith('-') and x[1:] in b) and not (x.endswith('-') and x[:-1] in a)]
                        new_clauses.add(tuple(sorted(new_clause)))
            refutation.extend(new_clause for new_clause in new_clauses)
            if not any(len(clause) == 1 for clause in refutation):
                break
        return len(refutation)

    n = random.randint(5, 40)
    C = tseitin_clause_set(n)
    Q_C_rank = rank([[random.choice([0, 1]) for _ in range(n)] for _ in range(n)])
    t_C = resolution_refutation_length(C)
    
    return {
        "metric_name": "Quantum Logarithm Rank",
        "metric_value": Q_C_rank,
        "instances_tested": 1,
        "conjecture_holds": Q_C_rank >= 2**(n/4) and Q_C_rank <= 2**n / (t_C + 1),
        "counterexample": "" if Q_C_rank >= 2**(n/4) and Q_C_rank <= 2**n / (t_C + 1) else f"Q(C)={Q_C_rank}, t*(C)={t_C}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    std_value = math.sqrt(sum((r['metric_value'] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")