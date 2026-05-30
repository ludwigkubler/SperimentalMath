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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment, literals):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and -literal in assignment or literal > 0 and literal in assignment:
                return False
            assignment[literal] = True if literal > 0 else False
            literals.remove(literal)
            clauses = [c for c in clauses if literal not in c and -literal not in c]
            return dpll(clauses, assignment, literals)
        pure_literal = next((l for l in literals if all(l in clause or -l in clause for clause in clauses)), None)
        if pure_literal:
            assignment[pure_literal] = True
            literals.remove(pure_literal)
            clauses = [c for c in clauses if pure_literal not in c and -pure_literal not in c]
            return dpll(clauses, assignment, literals)
        literal = random.choice(literals)
        assignment[literal] = True
        literals.remove(literal)
        if dpll(clauses, assignment, literals):
            return True
        assignment[literal] = False
        literals.add(literal)
        assignment[-literal] = True
        literals.remove(-literal)
        if dpll(clauses, assignment, literals):
            return True
        return False
    
    def literal_frequencies(proof):
        freqs = {}
        for clause in proof:
            for lit in clause:
                if lit not in freqs:
                    freqs[lit] = 0
                freqs[lit] += 1
        total_clauses = len(proof)
        return {lit: count / total_clauses for lit, count in freqs.items()}
    
    def kendall_tau_distance(freqs):
        n = sum(freqs.values())
        tau_numerator = 0
        for i in range(n):
            for j in range(i + 1, n):
                if freqs[i] != freqs[j]:
                    tau_numerator += (freqs[i] - freqs[j]) * (i - j)
        return abs(tau_numerator) / (n * (n - 1) / 2)
    
    def resolution_proof(clauses):
        literals = set(abs(lit) for clause in clauses for lit in clause)
        assignment = {}
        proof = []
        while True:
            if dpll(clauses, assignment, literals):
                return proof
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if not unit_clause:
                break
            literal = unit_clause[0]
            proof.append([literal])
            literals.remove(literal)
            clauses = [c for c in clauses if literal not in c and -literal not in c]
        return proof
    
    n = random.randint(5, 40)
    clauses = generate_3cnf(n)
    proof = resolution_proof(clauses)
    freqs = literal_frequencies(proof)
    tau_distance = kendall_tau_distance(freqs)
    
    return {
        "metric_name": "Kendall tau distance",
        "metric_value": tau_distance,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": tau_distance <= n**0.5 + 1 and tau_distance >= n**0.5 - 0.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Kendall tau distance does not match conjecture' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")