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
    
    def dpll(circuit):
        if not circuit:
            return True, []
        var = next((v for v in range(len(circuit[0])) if any(v in clause for clause in circuit)), None)
        if var is None:
            return False, []
        
        def propagate(lit, assignment):
            new_circuit = []
            for clause in circuit:
                if lit not in clause and -lit not in clause:
                    new_clause = [l for l in clause if l != -lit]
                    if not new_clause:
                        return False, []
                    new_circuit.append(new_clause)
            return True, assignment + [lit]
        
        def backtrack():
            for value in [-1, 1]:
                assignment = propagate(value * var, [])
                if assignment and dpll(circuit):
                    return True
            return False
        
        return backtrack()
    
    def tropicalized_heegaard_rank(circuit):
        n = len(circuit[0])
        rank = 0
        for i in range(n):
            if any(var == i for var, _ in circuit):
                rank += 1
        return rank
    
    def size(circuit):
        return sum(len(clause) for clause in circuit)
    
    c = random.randint(5, 40)
    n = 2 ** c
    circuit = []
    for _ in range(n):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        if all(lit not in clause and -lit not in clause for lit in circuit):
            circuit.append(clause)
    
    rank = tropicalized_heegaard_rank(circuit)
    size_circuit = size(circuit)
    c_const = 0.5
    
    return {
        "metric_name": "rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank >= c_const * math.log(size_circuit),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 1 for i in range(5, 6)]
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mapping_undefined"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")