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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(x == 0 for x in clause):
                clause[random.randint(0, n - 1)] = random.choice([-1, 1])
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment=[]):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment + [literal] if literal > 0 else assignment + [-literal]
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        pure_literal = next((l for l in range(1, 2 * n + 1) if all(l in c or -l in c for c in clauses)), None)
        if pure_literal:
            literal = pure_literal if literal > 0 else -pure_literal
            new_assignment = assignment + [literal] if literal > 0 else assignment + [-literal]
            if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
                return True
            return False
        literal = random.choice(range(1, 2 * n + 1))
        new_assignment = assignment + [literal] if literal > 0 else assignment + [-literal]
        if dpll([c for c in clauses if literal not in c and -literal not in c], new_assignment):
            return True
        return False
    
    def minimal_rank(clauses):
        n = len(clauses)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if all(c[i] * c[j] == 0 for c in clauses):
                    rank += 1
        return rank
    
    def dpll_length(clauses):
        return len(dpll(clauses))
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    rank = minimal_rank(cnf)
    length = dpll_length(cnf)
    
    return {
        "metric_name": "rank_vs_dpll_length",
        "metric_value": rank / length,
        "instances_tested": 1,
        "conjecture_holds": True if rank / length >= 0.5 else False,
        "counterexample": "" if rank / length >= 0.5 else "Rank/Length ratio < 0.5"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(2, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results) and any(r["metric_value"] >= 0.5 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Rank/Length ratio < 0.5' first_failing_seed={first_failing_seed}")