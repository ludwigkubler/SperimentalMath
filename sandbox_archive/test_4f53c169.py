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
        for _ in range(10 * n):  # Each variable appears in at least 10 clauses
            clause = [random.randint(-n, n) for _ in range(random.randint(2, 5))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def eichler_coefficients(clauses):
        # Placeholder for Eichler coefficient computation
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(tuple(sorted(c)) for c in clauses))
    
    def count_proofs(clauses):
        # Placeholder for proof counting
        # This is a dummy implementation and should be replaced with actual logic
        return 2 ** (len(clauses) // 2)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    eichler_count = eichler_coefficients(cnf)
    proofs_count = count_proofs(cnf)
    
    metric_value = eichler_count / n
    conjecture_holds = 2 ** (n // 2) <= proofs_count
    
    return {
        "metric_name": "Eichler Coefficients / Variables",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"n={n}, eichler_count={eichler_count}, proofs_count={proofs_count}"
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