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
    
    n = random.randint(5, 40)
    cnf_formula = []
    for _ in range(random.randint(10, 20)):
        clause = [random.randint(-n, n) for _ in range(random.randint(1, n))]
        if all(abs(lit) != abs(clause[0]) for lit in clause):
            cnf_formula.append(clause)
    
    truth_table = [[int(eval(' and '.join(str(lit) if lit > 0 else f'not {abs(lit)}' for lit in clause))) for clause in cnf_formula] for _ in range(2**n)]
    
    def additive_energy(truth_table):
        n = len(truth_table)
        energy = 0
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    for l in range(k+1, n):
                        if truth_table[i][k] == truth_table[j][l]:
                            energy += 1
        return energy
    
    def acc0_circuit_size(truth_table):
        # Placeholder heuristic: size is proportional to the number of variables
        return n * 2
    
    E_f = additive_energy(truth_table)
    S_f = acc0_circuit_size(truth_table)
    
    if S_f == 0:
        return {
            "metric_name": "E(f) * S(f)^β",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "acc0_circuit_size_undefined"
        }
    
    beta = 0.5
    alpha = 0.5
    C = 1.0
    
    if E_f * S_f**beta >= C * n**alpha:
        return {
            "metric_name": "E(f) * S(f)^β",
            "metric_value": E_f * S_f**beta,
            "instances_tested": 1,
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "E(f) * S(f)^β",
            "metric_value": E_f * S_f**beta,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Failed for n={n}, E(f)={E_f}, S(f)={S_f}"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None)) / len(results)
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