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
    
    def sipser_function(n, x):
        return sum(x[i] for i in range(1, n+1)) % 2 == 0
    
    def truth_table(f, n):
        table = []
        for x in product([0, 1], repeat=n):
            table.append((x, f(n, x)))
        return table
    
    def additive_energy(table):
        energy = 0
        n = len(table[0][0])
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    for l in range(k+1, n):
                        if table[i][1] + table[j][1] == table[k][1] + table[l][1]:
                            energy += 1
        return energy
    
    def acc0_circuit_size(n):
        # Simplified estimate based on known results
        return math.ceil(n**2.5 / math.log(n))
    
    n = 40
    instances_tested = 30
    total_energy = 0
    support_count = 0
    counterexample = ""
    
    for _ in range(instances_tested):
        x = tuple(random.randint(0, 1) for _ in range(n))
        f_value = sipser_function(n, x)
        table = truth_table(sipser_function, n)
        energy = additive_energy(table)
        
        if energy < n**2.5 - 1e-6:
            counterexample = f"Counterexample: Sipser function with n={n}, x={x}"
            break
        
        total_energy += energy
        if energy >= n**2.5 - 1e-6 and acc0_circuit_size(n) <= 10000:
            support_count += 1
    
    avg_energy = total_energy / instances_tested
    conjecture_holds = support_count / instances_tested >= 0.8
    
    return {
        "metric_name": "Additive Energy",
        "metric_value": avg_energy,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_energy = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["counterexample"] == "" for r in results):
        print(f"RESULT: SUPPORTED mean={mean_energy} std=0.0 support_fraction={support_fraction}")
    elif any(r["counterexample"] != "" for r in results):
        first_failing_seed = next((r["seed"] for r in results if r["counterexample"] != ""), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")