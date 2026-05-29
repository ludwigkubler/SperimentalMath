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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0], clause[1] = -clause[0], -clause[1]
            cnf.append(clause)
        return cnf
    
    def resolution(cnf):
        clauses = set(tuple(sorted(c)) for c in cnf)
        new_clauses = []
        while True:
            new_clause = None
            for c1, c2 in itertools.combinations(clauses, 2):
                if any(-x in c2 for x in c1):
                    new_clause = tuple(sorted(set(c1) - {-c} for c in c2))
                    break
            if not new_clause:
                break
            clauses.add(new_clause)
        return len(clauses)
    
    def count_arithmetic_progressions(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        progressions = 0
        for i in range(1, n + 1):
            for j in range(i + 3, n + 1):
                if (j - i) % 2 == 0:
                    diff = (j - i) // 2
                    if all(lit in {i, j} or lit in {-i, -j} for clause in cnf for lit in clause):
                        progressions += 1
        return progressions
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    cnf = generate_cnf(n, m)
    t_F = resolution(cnf)
    P_F = count_arithmetic_progressions(cnf)
    
    alpha = 1.0
    metric_value = P_F / math.log(t_F + 1) if t_F > 0 else float('inf')
    
    return {
        "metric_name": "E[|P(F)|] / log(t*(F))",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": P_F <= alpha * math.log(t_F + 1),
        "counterexample": "" if P_F <= alpha * math.log(t_F + 1) else f"Found counterexample with n={n}, m={m}, t*(F)={t_F}, |P(F)|={P_F}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
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
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")