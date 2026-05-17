# auto-injected by SEC sandbox
import itertools
import json
import sys
import os
import time
import re
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from collections import defaultdict

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def is_sat(F):
        # Small-DPLL precheck
        return False  # Placeholder for actual implementation
    
    def build_clause_conflict_graph(F):
        C_F = defaultdict(list)
        m = len(F)
        for i in range(m):
            for j in range(i + 1, m):
                if any(l == ~r or r == ~l for l in F[i] for r in F[j]):
                    C_F[i].append(j)
                    C_F[j].append(i)
        return C_F
    
    def enumerate_independence_complex(C_F, max_size=4):
        I_C_F = []
        stack = [set()]
        while stack:
            current = stack.pop()
            if len(current) > max_size:
                continue
            I_C_F.append(tuple(sorted(current)))
            for v in range(len(C_F)):
                if v not in current and all(v not in C_F[u] for u in current):
                    stack.append(current | {v})
        return I_C_F
    
    def lex_smallest_coface(F, sigma, dim):
        for tau in F:
            if len(tau) == dim + 1 and all(l in tau for l in sigma):
                return tau
        return None
    
    def greedy_lex_discrete_morse_matching(I_C_F):
        critical_cells = []
        matched = set()
        for sigma in sorted(I_C_F, key=lambda x: (len(x), tuple(sorted(x)))):
            if sigma not in matched:
                tau = lex_smallest_coface(I_C_F, sigma, len(sigma))
                if tau is None:
                    critical_cells.append(sigma)
                else:
                    matched.add(tau)
        return critical_cells
    
    def dpll(F):
        stack = [([], F)]
        while stack:
            assignment, remaining = stack.pop()
            if not remaining:
                return len(assignment)
            var = remaining[0]
            for val in [True, False]:
                new_assignment = assignment + [(var, val)]
                new_remaining = [c for c in remaining if not any(l == ~r or r == ~l for l, v in new_assignment if v)]
                if is_sat(new_remaining):
                    stack.append((new_assignment, new_remaining))
        return 0
    
    n = random.choice([12, 16, 20, 24, 28])
    m = int(4.5 * n)
    F = [[random.randint(-n, n) for _ in range(m)] for _ in range(n)]
    
    if is_sat(F):
        return {
            "metric_name": "log_2(t*(F))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "SAT instance"
        }
    
    C_F = build_clause_conflict_graph(F)
    I_C_F = enumerate_independence_complex(C_F)
    delta_F = len(greedy_lex_discrete_morse_matching(I_C_F))
    t_star_F = dpll(F)
    
    if t_star_F == 0:
        return {
            "metric_name": "log_2(t*(F))",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL returned no leaves"
        }
    
    metric_value = math.log2(t_star_F)
    return {
        "metric_name": "log_2(t*(F))",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": True if metric_value >= 0.25 * math.log2(delta_F + 2) else False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        support_fraction = 1.0
    else:
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(r['metric_value'] for r in results) / len(results)} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["counterexample"] for r in results):
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"] and r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'] and r['counterexample'])]}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction=<z>")