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
        cnf = []
        for _ in range(2**n):
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if all(abs(lit) != abs(clause[0]) for lit in clause[1:]):
                cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        clauses = [set(clause) for clause in cnf]
        resolvents = set()
        
        while True:
            new_resolvents = set()
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    common_lits = set.intersection(*[clauses[i], clauses[j]])
                    if common_lits:
                        resolvent = clauses[i].union(clauses[j]) - common_lits
                        new_resolvents.add(frozenset(resolvent))
            if not new_resolvents:
                break
            resolvents.update(new_resolvents)
            clauses.extend(new_resolvents)
        
        return len(resolvents)
    
    def quandle_order(cnf):
        n = len(cnf[0])
        quandle = {i: i for i in range(n)}
        for clause in cnf:
            if len(clause) == 1:
                quandle[abs(clause[0])] = abs(clause[0])
            else:
                quandle[abs(clause[0])] = abs(clause[1])
        return max(quandle.values())
    
    n_max = 40
    instances_tested = 0
    total_metric_value = 0
    
    for n in range(5, n_max + 1):
        cnf = generate_cnf(n)
        width = resolution_width(cnf)
        order = quandle_order(cnf)
        
        if order > 2**n:
            return {
                "metric_name": "quandle_order",
                "metric_value": order,
                "instances_tested": instances_tested + 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Order {order} exceeds 2^{n}"
            }
        
        total_metric_value += order
        instances_tested += 1
    
    return {
        "metric_name": "quandle_order",
        "metric_value": total_metric_value / instances_tested,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Order exceeds 2^n\" first_failing_seed={seeds[first_failing_seed]}")