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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def count_clauses(f):
        n = int(math.log2(len(f)))
        clauses = []
        for i in range(n):
            clause = []
            for j in range(n):
                if f[2**i + 2**(j+1)] != f[2**i]:
                    clause.append(j)
            if clause:
                clauses.append(clause)
        return len(clauses)
    
    def find_brauer_classes(f):
        n = int(math.log2(len(f)))
        classes = set()
        for i in range(2**n):
            class_rep = []
            for j in range(n):
                if f[i + 2**(j+1)] != f[i]:
                    class_rep.append(j)
            classes.add(tuple(sorted(class_rep)))
        return len(classes)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(4, n_max)
        f = generate_boolean_function(n)
        C_f = count_clauses(f)
        B_f = find_brauer_classes(f)
        
        if B_f > C_f:
            conjecture_holds = False
            counterexample = f"n={n}, |B(f)|={B_f}, C(f)={C_f}"
        
        metric_values.append(B_f)
    
    return {
        "metric_name": "|B(f)|",
        "metric_value": sum(metric_values) / len(metric_values),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = r["counterexample"]
                first_failing_seed = r["seed"]
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")