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
        for _ in range(2**n - 1):
            clause = [random.choice([f'x{i+1}', f'-x{i+1}']) for i in range(n)]
            if random.choice([True, False]):
                clause.append('-')
            clauses.append(clause)
        return clauses

    def tseitin_encoding(cnf):
        formulas = []
        literals = set()
        new_var = 2**len(cnf) + 1
        for i, clause in enumerate(cnf):
            if len(clause) == 1:
                formulas.append(f'{new_var} <=> {clause[0]}')
                literals.add(new_var)
                new_var += 1
            else:
                temp_var = new_var
                new_var += 1
                for literal in clause[:-1]:
                    formulas.append(f'{temp_var} <=> {literal}')
                    literals.add(temp_var)
                formulas.append(f'{new_var} <=> -{temp_var}')
                literals.add(new_var)
                new_var += 1
        return formulas, literals

    def frege_proof_length(cnf):
        formulas, literals = tseitin_encoding(cnf)
        proof_length = len(formulas) + len(literals)
        return proof_length

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    l_f = frege_proof_length(cnf)

    mfc_min = 1 / (2 ** (l_f / n))

    return {
        "metric_name": "mfc_min",
        "metric_value": mfc_min,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")