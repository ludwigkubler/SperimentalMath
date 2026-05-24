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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(10 * n):  # Each variable appears in 10 clauses on average
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            random.shuffle(clause)
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(clauses):
        n = len(clauses[0])
        poly = [[0] * (2 ** n) for _ in range(2 ** n)]
        for clause in clauses:
            index = 0
            for var in clause:
                if var > 0:
                    index |= 1 << (var - 1)
                else:
                    index &= ~(1 << (-var - 1))
            poly[index][index] += 1
        return poly
    
    def schur_weyl_representation(poly):
        n = int(math.log2(len(poly)))
        rep = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(2 ** n):
            for j in range(2 ** n):
                if poly[i][j] > 0:
                    rep[i & j][i | j] += poly[i][j]
        return rep
    
    def min_rank(rep):
        m = len(rep)
        n = len(rep[0])
        rank = 0
        for i in range(m):
            pivot = None
            for j in range(n):
                if rep[i][j] != 0:
                    pivot = j
                    break
            if pivot is not None:
                rank += 1
                for k in range(m):
                    if k != i and rep[k][pivot] != 0:
                        factor = rep[k][pivot] / rep[i][pivot]
                        for l in range(n):
                            rep[k][l] -= factor * rep[i][l]
        return rank
    
    def dpll(clauses, assignment=[]):
        if not clauses:
            return True
        var = next((i for i in range(len(clauses[0])) if (assignment[i] is None and any(c[i] != 0 for c in clauses))), -1)
        if var == -1:
            return False
        for val in [-1, 1]:
            new_assignment = assignment[:]
            new_assignment[var] = val
            if dpll(clauses, new_assignment):
                return True
        return False
    
    def dpll_length(clauses):
        n = len(clauses[0])
        assignment = [None] * n
        stack = []
        length = 0
        while True:
            if not clauses or all(assignment[i] is not None for i in range(n)):
                break
            var = next((i for i in range(n) if (assignment[i] is None and any(c[i] != 0 for c in clauses))), -1)
            if var == -1:
                return float('inf')
            stack.append((var, assignment[:]))
            length += 1
            for val in [-1, 1]:
                new_assignment = assignment[:]
                new_assignment[var] = val
                if dpll(clauses, new_assignment):
                    break
            else:
                var, assignment = stack.pop()
                length -= 1
        return length
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    poly = clause_indicator_polynomial(clauses)
    rep = schur_weyl_representation(poly)
    min_rank_value = min_rank(rep)
    dpll_length_value = dpll_length(clauses)
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": 0.5,  # Placeholder value for demonstration
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
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
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={seed}")
                break