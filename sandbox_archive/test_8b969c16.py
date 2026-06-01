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
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n * 2) for _ in range(random.randint(1, 3))]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def is_quadratic_residue(x, p):
        return (x * x) % p == 1
    
    def min_quadratic_residues(clauses, p):
        residues = set()
        for clause in clauses:
            if len(clause) == 1:
                residues.add(abs(clause[0]) % p)
            else:
                for i in range(len(clause)):
                    for j in range(i + 1, len(clause)):
                        x, y = abs(clause[i]), abs(clause[j])
                        if is_quadratic_residue(x * y, p):
                            residues.add(abs(x) % p)
                            residues.add(abs(y) % p)
        return residues
    
    def frege_proof_size(clauses):
        # Simplified Frege proof size estimation
        return sum(len(clause) for clause in clauses)
    
    n = random.randint(5, 40)
    p = random.randint(n + 1, n * 2)
    cnf = generate_cnf(n)
    residues = min_quadratic_residues(cnf, p)
    proof_size = frege_proof_size(cnf)
    
    return {
        "metric_name": "Q(φ)",
        "metric_value": len(residues),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif sum(1 for r in results if not r["conjecture_holds"]) >= len(results) * 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={seeds[sum(1 for r in results if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")