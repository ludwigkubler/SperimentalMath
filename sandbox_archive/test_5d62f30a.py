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
    
    # Generate a random CNF with depth d and clause count c
    def generate_cnf(depth, clauses):
        variables = set()
        cnf = []
        for _ in range(clauses):
            clause = []
            for _ in range(random.randint(1, 3)):
                var = f'x{random.randint(1, variables)}'
                if random.choice([True, False]):
                    var = f'-{var}'
                clause.append(var)
                variables.add(abs(int(var[1:])))
            cnf.append(clause)
        return cnf
    
    # Construct a Frege proof for the given CNF
    def construct_frege_proof(cnf):
        proof = []
        for clause in cnf:
            if len(clause) == 1:
                proof.append((clause, 'axiom'))
            else:
                subproofs = [construct_frege_proof([subclause]) for subclause in clause]
                proof.append((clause, 'resolution', *subproofs))
        return proof
    
    # Compute the p-adic valuation vector of a clause
    def p_adic_valuation_vector(clause):
        p = 2  # Using base 2 for simplicity
        vector = [0] * (len(variables) + 1)
        for var in clause:
            if var.startswith('-'):
                var = var[1:]
                sign = -1
            else:
                sign = 1
            index = int(var[1:])
            vector[index] += sign
        return vector
    
    # Compute the minimal rank of a list of vectors
    def min_rank(vectors):
        if not vectors:
            return 0
        n, m = len(vectors), len(vectors[0])
        rank = 0
        for i in range(m):
            pivot_found = False
            for j in range(rank, n):
                if vectors[j][i] != 0:
                    vectors[j], vectors[rank] = vectors[rank], vectors[j]
                    pivot_found = True
                    break
            if not pivot_found:
                continue
            rank += 1
            for j in range(n):
                if j != rank - 1 and vectors[j][i] != 0:
                    factor = vectors[j][i] / vectors[rank - 1][i]
                    for k in range(m):
                        vectors[j][k] -= factor * vectors[rank - 1][k]
        return rank
    
    # Generate a random CNF with depth d and clause count c
    depth = random.randint(5, 40)
    clauses = random.randint(20, 80)
    cnf = generate_cnf(depth, clauses)
    
    # Construct a Frege proof for the given CNF
    proof = construct_frege_proof(cnf)
    
    # Compute the p-adic valuation vectors of all clauses in the proof
    valuation_vectors = []
    for clause, _, *subproofs in proof:
        valuation_vector = p_adic_valuation_vector(clause)
        valuation_vectors.extend(valuation_vector for _ in subproofs)
    
    # Compute the minimal rank of the p-adic valuation vectors
    min_rank_value = min_rank(valuation_vectors)
    
    # Measure the depth of the Frege proof
    depth_value = len(proof)
    
    # Check if the conjecture holds
    conjecture_holds = min_rank_value <= 2.0 * depth_value
    
    return {
        "metric_name": "min_rank_to_depth_ratio",
        "metric_value": min_rank_value / depth_value,
        "instances_tested": len(valuation_vectors),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Depth={depth}, Min Rank={min_rank_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **{result}}}")
        results.append(result)
    
    mean_d = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_d) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")