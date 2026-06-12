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
    
    def satisfiable_points(phi):
        n = len(phi) // (next(k for k in phi if k.startswith('v'))[1:])
        points = []
        for i in range(2**n):
            point = [int(bit) for bit in format(i, f'0{n}b')]
            if all(point[j] == 1 or phi[j].endswith(f'!{point[j]}') for j in range(n)):
                points.append(tuple(point))
        return points
    
    def quasi_closed_set(points):
        n = len(points[0])
        qcs = set()
        for point in points:
            qcs.add(point)
            for i in range(n):
                if point[i] == 1:
                    new_point = list(point)
                    new_point[i] = 0
                    qcs.add(tuple(new_point))
        return qcs
    
    def resolution_proof_depth(phi, points):
        n = len(points[0])
        clauses = [set() for _ in range(n)]
        for point in points:
            for i in range(n):
                if point[i] == 1:
                    clauses[i].add(i)
        
        stack = []
        while True:
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                break
            literal = list(unit_clause)[0]
            stack.append(literal)
            for i in range(n):
                if i != literal and -i not in stack:
                    clauses[i].discard(-literal)
        
        return len(stack)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        phi = ['v' + str(i+1) if i % 2 == 0 else '!v' + str(i+1) for i in range(n)]
        points = satisfiable_points(phi)
        qcs = quasi_closed_set(points)
        d_phi = resolution_proof_depth(phi, points)
        omega_phi = len(qcs)
        
        metric_values.append(d_phi / omega_phi)
    
    mean_value = sum(metric_values) / instances_tested
    std_dev = math.sqrt(sum((x - mean_value)**2 for x in metric_values) / instances_tested)
    
    if any(value < 0.8 * mean_value or value > 3 + mean_value for value in metric_values):
        conjecture_holds = False
        counterexample = "correlation_coefficient_out_of_bounds"
    
    return {
        "metric_name": "resolution_proof_depth_over_omega",
        "metric_value": mean_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient_out_of_bounds' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_support")