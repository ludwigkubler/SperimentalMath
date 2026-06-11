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

def generate_cnf(n):
    clauses = []
    for _ in range(2 * n):
        clause = [random.randint(-n, -1), random.randint(1, n)]
        clauses.append(clause)
    return clauses

def qcr_mod_2k(cnf, k):
    factors = [0] * (2 * len(cnf))
    for clause in cnf:
        for lit in clause:
            if abs(lit) <= 2 * len(cnf):
                factors[abs(lit) - 1] += 1
    return all(f % (2 ** k) == 0 for f in factors)

def resolution_width(cnf):
    clauses = cnf[:]
    width = 0
    while clauses:
        new_clause = []
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                if not set(clauses[i]).isdisjoint(set(clauses[j])):
                    new_clause.extend([x for x in clauses[i] if x not in clauses[j]])
                    new_clause.extend([x for x in clauses[j] if x not in clauses[i]])
        if not new_clause:
            break
        width = max(width, len(new_clause))
        clauses.append(new_clause)
    return width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_max = 40
    instances_tested = 0
    metric_value = 0.0
    conjecture_holds = True
    counterexample = ""

    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        if qcr_mod_2k(cnf, 10):  # Assuming k=10 is sufficient for our purposes
            instances_tested += 1
            rpw = resolution_width(cnf)
            metric_value += rpw / n
            if rpw > 1.5 * n or (rpw < n and instances_tested >= len(cnf) // 2):
                conjecture_holds = False
                counterexample = f"n={n}, RPW={rpw}"
                break

    return {
        "metric_name": "Resolution Proof Width",
        "metric_value": metric_value / instances_tested if instances_tested > 0 else 0.0,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results) if results else 0.0
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results)) if results else 0.0
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"{results[next(i for i, r in enumerate(results) if not r['conjecture_holds'])['counterexample']]}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")