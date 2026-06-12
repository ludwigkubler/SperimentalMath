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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_k_cnf(k, n):
        cnf = []
        for _ in range(k):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def support(cnf, n):
        support_set = set()
        for clause in cnf:
            for lit in clause:
                if lit > 0:
                    support_set.add(lit)
                else:
                    support_set.discard(-lit)
        return support_set
    
    def geometric_lattice_size(support_set):
        lattice_size = len(support_set) + 1
        return lattice_size
    
    def frege_proof_length(cnf):
        # Simplified estimation of Frege proof length
        return len(cnf) * 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_lattices = 0
    total_proofs = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            k = random.randint(1, min(n, 10))
            cnf = generate_k_cnf(k, n)
            support_set = support(cnf, n)
            lattice_size = geometric_lattice_size(support_set)
            proof_length = frege_proof_length(cnf)
            
            total_lattices += lattice_size
            total_proofs += proof_length
            instances_tested += 1
            n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_lattices = Fraction(total_lattices, instances_tested)
    mean_proofs = Fraction(total_proofs, instances_tested)
    correlation_coefficient = (mean_lattices * mean_proofs - total_lattices * total_proofs / instances_tested**2) / \
                               ((total_lattices**2 / instances_tested - mean_lattices**2) * (total_proofs**2 / instances_tested - mean_proofs**2))**0.5
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_lattices / mean_proofs <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_lattices = sum(r["metric_value"] * r["instances_tested"] for r in results if r["instances_tested"] > 0) / sum(r["instances_tested"] for r in results if r["instances_tested"] > 0)
    total_proofs = sum(r["metric_value"] * r["instances_tested"] for r in results if r["instances_tested"] > 0) / sum(r["instances_tested"] for r in results if r["instances_tested"] > 0)
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_lattices} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")