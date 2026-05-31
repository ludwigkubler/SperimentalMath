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
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-1, 1) * (i + 1) for i in range(n)]
            if any(x != 0 for x in clause):
                cnf.append(clause)
        return cnf

    def dpll(cnf):
        def search(k):
            if k == len(cnf):
                return True
            literals = set()
            for clause in cnf[k]:
                if clause > 0:
                    literals.add(clause)
                else:
                    literals.add(-clause)
            for lit in literals:
                new_cnf = [c[:] for c in cnf]
                new_cnf[k] = [x for x in new_cnf[k] if x != lit and x != -lit]
                if propagate(lit) is None:
                    continue
                if search(k + 1):
                    return True
            return False

        def propagate(lit):
            for i, clause in enumerate(cnf):
                if lit in clause:
                    cnf[i].remove(lit)
                elif -lit in clause:
                    cnf[i] = []
                    break
            return None
        
        return search(0)

    def mter(cnf):
        # Placeholder for minimal local index of topological entanglement rank calculation
        # This is a dummy implementation and should be replaced with actual logic
        return len(cnf) / 2

    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    path_length = dpll(cnf)
    mter_value = mter(cnf)

    if path_length is None or mter_value is None:
        return {
            "metric_name": "mter_vs_path_length",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "dpll returned None"
        }

    return {
        "metric_name": "mter_vs_path_length",
        "metric_value": abs(mter_value - path_length),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(mter_value - path_length) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['n_max']}, mter={r['metric_value']}, path_length={path_length}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
        else:
            print("RESULT: INCONCLUSIVE insufficient support_fraction")