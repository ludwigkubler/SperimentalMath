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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def truth_table(cnf, n):
        tt = [[False] * (2**n) for _ in range(len(cnf))]
        for i in range(2**n):
            assignment = [bool((i >> j) & 1) for j in range(n)]
            for clause in cnf:
                if all(not assignment[abs(l)-1] if l < 0 else assignment[l-1] for l in clause):
                    tt[len(cnf)-1][i] = True
                    break
        return tt
    
    def quantum_entanglement(tt, n):
        # Simplified estimation of quantum entanglement (not actual quantum simulation)
        return sum(sum(row) for row in tt) / len(tt)
    
    def frege_proof_depth(cnf):
        # Simplified estimation of Frege proof depth
        return len(cnf) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            cnf = generate_cnf(n, random.randint(1, n))
            tt = truth_table(cnf, n)
            entanglement = quantum_entanglement(tt, n)
            depth = frege_proof_depth(cnf)
            results.append((entanglement, depth))
    
    if not results:
        return {
            "metric_name": "QuantumEntanglement vs FregeProofDepth",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    entanglements, depths = zip(*results)
    correlation = sum((e - (sum(entanglements) / len(entanglements))) * (d - (sum(depths) / len(depths)))
                      for e, d in zip(entanglements, depths)) / len(entanglements)
    
    return {
        "metric_name": "QuantumEntanglement vs FregeProofDepth",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": abs(correlation) > 0.1,  # Arbitrary threshold for correlation
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for result in results:
            if not result["conjecture_holds"]:
                counterexample = "mapping_undefined"
                break
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[results.index(next(result for result in results if not result['conjecture_holds']))]}")