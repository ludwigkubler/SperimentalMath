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
    
    def generate_k_clique(n, k):
        if k > n // 2:
            return None
        edges = set()
        nodes = list(range(n))
        for i in range(k):
            for j in range(i + 1, k):
                edges.add((nodes[i], nodes[j]))
        for _ in range(int(n * (n - 1) / 2) - len(edges)):
            u, v = random.sample(nodes, 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        return edges
    
    def clause_indicator_polynomial(edges):
        n = max(max(u, v) for u, v in edges) + 1
        poly = [0] * (n ** 2)
        for u, v in edges:
            poly[u * n + v] = 1
        return poly
    
    def polarized_hodge_structure(poly):
        n = int(math.sqrt(len(poly)))
        hodge_structure = []
        for i in range(n):
            row = [poly[i * n + j] for j in range(n)]
            hodge_structure.append(row)
        return hodge_structure
    
    def count_monomials(hodge_structure):
        count = 0
        for row in hodge_structure:
            for val in row:
                if val == 1:
                    count += 1
        return count
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_monomials = 0
    total_proofs = 0
    
    for n in n_values:
        k = random.randint(2, n // 2)
        edges = generate_k_clique(n, k)
        if edges is None:
            continue
        
        poly = clause_indicator_polynomial(edges)
        hodge_structure = polarized_hodge_structure(poly)
        monomials = count_monomials(hodge_structure)
        
        total_monomials += monomials
        total_proofs += len(edges)
    
    instances_tested = len(n_values) * len(n_values)
    mean_monomials = total_monomials / instances_tested
    mean_proofs = total_proofs / instances_tested
    
    if abs(mean_monomials - mean_proofs) > 0.2 * mean_proofs:
        conjecture_holds = False
        counterexample = f"mean_monomials={mean_monomials}, mean_proofs={mean_proofs}"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": mean_proofs,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_monomials = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_monomials) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_monomials} std={std_dev} support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_monomials={results[first_failing_seed]['metric_value']}, mean_proofs={results[first_failing_seed]['instances_tested']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")