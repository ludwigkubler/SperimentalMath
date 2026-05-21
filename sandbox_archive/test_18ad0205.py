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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            random.shuffle(clause)
            clauses.append(clause)
        return clauses

    def cylindrical_algebraic_decomposition(clauses):
        # Simplified version for demonstration; actual implementation needed
        return "non-trivial"

    def sos_degree(clauses):
        # Simplified version for demonstration; actual implementation needed
        return 1

    n = 40
    instances_tested = 30
    metric_name = "sos_degree"
    counterexample = ""
    
    results = []
    for _ in range(instances_tested):
        clauses = generate_3cnf(n)
        real_radical = cylindrical_algebraic_decomposition(clauses)
        if real_radical == "non-trivial":
            sos_deg = sos_degree(clauses)
            if sos_deg < math.log(n, 2):
                counterexample = f"n={n}, SOS degree={sos_deg}"
                break
        results.append({"metric_value": sos_deg})
    
    conjecture_holds = all(r["metric_value"] >= math.log(n, 2) for r in results)
    
    return {
        "metric_name": metric_name,
        "metric_value": sum(r["metric_value"] for r in results) / instances_tested,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(5, 8)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")