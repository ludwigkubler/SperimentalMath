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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            if all(abs(x) != abs(y) for x, y in itertools.combinations(clause, 2)):
                clauses.append(clause)
        return clauses
    
    def cnf_to_vector_space(cnf):
        n = max(abs(var) for clause in cnf for var in clause)
        V = [[0] * (n + 1) for _ in range(2**n)]
        for i, clause in enumerate(cnf):
            for var in clause:
                if var > 0:
                    V[i][var] = 1
                else:
                    V[i][-var] = -1
        return V
    
    def gaussian_elimination(V):
        m, n = len(V), len(V[0])
        rank = 0
        for j in range(n):
            i_max = next((i for i in range(rank, m) if V[i][j]), None)
            if i_max is not None:
                V[rank], V[i_max] = V[i_max], V[rank]
                for i in range(rank + 1, m):
                    factor = Fraction(V[i][j], V[rank][j])
                    for k in range(n):
                        V[i][k] -= factor * V[rank][k]
                rank += 1
        return rank
    
    def bruer_group_rank(V):
        return gaussian_elimination(V)
    
    def resolution_refutation_depth(cnf):
        n = max(abs(var) for clause in cnf for var in clause)
        stack = []
        for clause in cnf:
            if all(x not in stack and -x not in stack for x in clause):
                stack.extend(clause)
            else:
                new_clause = [x for x in clause if x not in stack and -x not in stack]
                if not new_clause:
                    return 0
                stack.append(new_clause[0])
        return len(stack)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    V = cnf_to_vector_space(cnf)
    rho = bruer_group_rank(V)
    d = resolution_refutation_depth(cnf)
    
    conjecture_holds = rho >= 2**(n/4) and rho > n**1/8
    counterexample = "" if conjecture_holds else "rho <= n^1/8"
    
    return {
        "metric_name": "Brauer Group Rank vs Resolution Refutation Depth",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rho = sum(r["metric_value"] for r in results) / len(results)
    std_rho = math.sqrt(sum((r["metric_value"] - mean_rho)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rho} std={std_rho} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rho <= n^1/8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")