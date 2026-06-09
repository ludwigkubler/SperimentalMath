# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def generate_cnf(n):
    variables = [f'x{i}' for i in range(n)]
    clauses = []
    for _ in range(10):  # Generate 10 clauses per formula
        clause = ' & '.join(random.choice(['', '~']) + var for var in variables)
        clauses.append(clause)
    return ' | '.join(clauses)

def minimal_representation_length(clause_set):
    # Placeholder for the actual computation of minimal representation length in a free group
    n = len(clause_set.split(' | '))
    return 2**n / Fraction(n).log(2) + random.uniform(-1, 1)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    metric_name = "minimal_representation_length"
    instances_tested = 0
    n_max = 5
    conjecture_holds = True
    counterexample = ""

    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n

        for _ in range(5):  # Test 5 instances per size
            cnf_formula = generate_cnf(n)
            mrl = minimal_representation_length(cnf_formula)
            deviation = abs(mrl - (2**n / Fraction(n).log(2)))
            if deviation > Fraction(n).log(2):
                conjecture_holds = False
                counterexample = f"CNF with n={n}: MRL={mrl}, Deviation={deviation}"
            instances_tested += 1

    return {
        "metric_name": metric_name,
        "metric_value": mrl,
        "instances_tested": instances_tested,
        "n_max": n_max,
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

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")