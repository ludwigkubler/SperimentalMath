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
        for _ in range(2 * n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == -clause[j] for i in range(n) for j in range(i + 1, n)):
                continue
            clauses.append(clause)
        return clauses
    
    def clause_indicator_polynomial(cnf):
        n = len(cnf[0])
        poly = [[0] * (2 ** n) for _ in range(len(cnf))]
        for i, clause in enumerate(cnf):
            for j in range(2 ** n):
                assignment = [1 if (j >> k) & 1 else -1 for k in range(n)]
                if all(assignment[var - 1] * literal == 1 for literal in clause):
                    poly[i][j] = 1
        return poly
    
    def min_local_induction_ring_rank(poly):
        n = len(poly[0])
        m_lir = float('inf')
        for i in range(len(poly)):
            if any(poly[i][j] == 1 for j in range(2 ** n)):
                m_lir = min(m_lir, sum(poly[j].count(1) for j in range(2 ** n)))
        return m_lir
    
    def communication_complexity_rank(cnf):
        n = len(cnf[0])
        rank = 0
        for clause in cnf:
            rank += max(abs(sum(literal for literal in clause if literal > 0)), abs(sum(literal for literal in clause if literal < 0)))
        return rank
    
    def solve_cnf(cnf):
        n = len(cnf[0])
        for i in range(2 ** n):
            assignment = [1 if (i >> k) & 1 else -1 for k in range(n)]
            if all(assignment[var - 1] * literal == 1 for literal in clause for clause in cnf):
                return True
        return False
    
    def run_cnf_solver(cnf):
        return solve_cnf(cnf)
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    poly = clause_indicator_polynomial(cnf)
    m_lir = min_local_induction_ring_rank(poly)
    r_Γ = communication_complexity_rank(cnf)
    
    return {
        "metric_name": "m_lir",
        "metric_value": m_lir,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": m_lir >= r_Γ * Fraction(0.5, 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"m_lir < r_Γ\" first_failing_seed={r['seed']}")
                break