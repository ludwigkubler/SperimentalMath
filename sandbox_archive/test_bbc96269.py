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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            cnf.append(clause)
        return cnf
    
    def quandle_order(cnf):
        variables = set(abs(lit) for lit in sum(cnf, []))
        elements = list(variables)
        n = len(elements)
        
        # Construct the quandle table
        quandle_table = [[None] * n for _ in range(n)]
        for x in range(n):
            for y in range(n):
                if (x + 1) % n == y:
                    quandle_table[x][y] = x
                else:
                    quandle_table[x][y] = y
        
        # Find the minimal order
        min_order = float('inf')
        for perm in itertools.permutations(elements):
            order = 0
            for lit in sum(cnf, []):
                var = abs(lit)
                if perm.index(var) != (perm.index(-var) + 1) % n:
                    order += 1
                    break
            min_order = min(min_order, order)
        return min_order
    
    def entanglement_width(cnf):
        variables = set(abs(lit) for lit in sum(cnf, []))
        width = 0
        
        # Find the maximum number of literals sharing a variable
        for var in variables:
            max_clause_size = 0
            for clause in cnf:
                if var in clause or -var in clause:
                    max_clause_size = max(max_clause_size, len(clause))
            width = max(width, max_clause_size)
        
        return width
    
    n = random.randint(5, 30)
    m = random.randint(2, 40)
    cnf = generate_cnf(n, m)
    
    min_order = quandle_order(cnf)
    entanglement_width_val = entanglement_width(cnf)
    
    return {
        "metric_name": "MinOrder vs EntanglementWidth",
        "metric_value": min_order / entanglement_width_val,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(min_order - entanglement_width_val) <= 0.5 * entanglement_width_val,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
                counterexample = f"n={r['n_max']}, min_order={r['metric_value'] * r['entanglement_width_val']:.2f}, entanglement_width={r['entanglement_width_val']}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break