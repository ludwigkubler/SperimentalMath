import random
import itertools
import sys
from typing import List, Tuple, Set, Dict, Any, Generator
from functools import reduce
from collections import defaultdict
import math

# Note: This conjecture involves advanced algebraic geometry and proof complexity.
# Due to extreme computational complexity of computing splitting fields and Galois groups
# over function fields in characteristic 2, especially with Gröbner bases and factorization,
# a full implementation is infeasible with only standard libraries and within time limits.
#
# Instead, we simulate the test strategy at a small scale, using simplified proxies:
# - Use very small n (up to 4) due to combinatorial explosion.
# - Approximate resolution width via simple DPLL with width bounding.
# - Represent polynomials sparsely over F2, but cannot compute splitting fields or Galois groups.
# - Thus, we can only FALSIFY by finding a counterexample in small cases, or return INCONCLUSIVE.

random.seed(42)

def all_binary_vectors(n: int) -> List[Tuple[int, ...]]:
    return list(itertools.product([0, 1], repeat=n))

def evaluate_poly_in_f2(poly: List[Tuple[Tuple[int, ...], int]], 
                        x_vals: Tuple[int, ...], 
                        y_vals: Tuple[int, ...]) -> int:
    """Evaluate a multilinear polynomial over F2 given x and y assignments."""
    total = 0
    for monomial, coeff in poly:
        if coeff == 0:
            continue
        prod = 1
        for idx, power in enumerate(monomial):
            if power == 1:
                if idx < len(x_vals):
                    prod *= (x_vals[idx] if idx < len(x_vals) else y_vals[idx - len(x_vals)])
                else:
                    prod *= y_vals[idx - len(x_vals)]
        total ^= prod
    return total % 2

def clause_to_symmetric_poly(clause: List[Tuple[str, int]]) -> List[Tuple[Tuple[int, ...], int]]:
    """
    Convert a 3-CNF clause to symmetric multilinear polynomial over F2.
    Each literal: 'x_i' -> (1 + x_i), '¬x_i' -> (1 + y_i)
    But symmetrized: for literal l_i, we do (1 + a_i) where a_i is x_i or y_i,
    and include both the clause and its dual (swap x<->y).
    So: (l1 ∨ l2 ∨ l3) becomes:
        (1+a1)(1+a2)(1+a3) + (1+b1)(1+b2)(1+b3) where b_i swaps x<->y of a_i.
    Returns polynomial as list of (monomial_mask, coeff), coeff in F2.
    Monomial mask: tuple of 0/1 for each of x1..xn,y1..yn.
    """
    n_vars = max(abs(var) for _, var in clause)
    size = 2 * n_vars  # x1..xn, y1..yn
    poly = []

    # First term: use x_i for x_i, y_i for ¬x_i
    factors1 = []
    for sign, var in clause:
        idx = var - 1
        if sign == 'p':
            factors1.append(idx)  # x_i
        else:
            factors1.append(idx + n_vars)  # y_i
    # Expand (1 + v1)(1 + v2)(1 + v3)
    term1 = []
    for r in range(4):
        for combo in itertools.combinations(factors1, r):
            mono = [0] * size
            for i in combo:
                mono[i] = 1
            term1.append(tuple(mono))
    poly.extend([(m, 1) for m in term1])

    # Second term: swap x<->y
    factors2 = []
    for sign, var in clause:
        idx = var - 1
        if sign == 'p':
            factors2.append(idx + n_vars)  # y_i
        else:
            factors2.append(idx)  # x_i
    term2 = []
    for r in range(4):
        for combo in itertools.combinations(factors2, r):
            mono = [0] * size
            for i in combo:
                mono[i] = 1
            term2.append(tuple(mono))
    poly.extend([(m, 1) for m in term2])

    # Combine and reduce mod 2
    poly_dict = defaultdict(int)
    for mono, coeff in poly:
        poly_dict[mono] ^= coeff
    return [(k, v) for k, v in poly_dict.items() if v == 1]

def build_phi_polynomial(clauses: List[List[Tuple[str, int]]]) -> List[Tuple[Tuple[int, ...], int]]:
    """Build p_φ as sum of symmetrized clause polynomials."""
    if not clauses:
        return []
    poly_sum = []
    for clause in clauses:
        clause_poly = clause_to_symmetric_poly(clause)
        poly_sum.extend(clause_poly)
    # Combine mod 2
    poly_dict = defaultdict(int)
    for mono, coeff in poly_sum:
        poly_dict[mono] ^= coeff
    return [(k, v) for k, v in poly_dict.items() if v == 1]

def simplify_poly(poly: List[Tuple[Tuple[int, ...], int]]) -> List[Tuple[Tuple[int, ...], int]]:
    """Remove zero coefficients and sort."""
    poly_dict = defaultdict(int)
    for mono, coeff in poly:
        poly_dict[mono] ^= coeff
    return sorted([(k, v) for k, v in poly_dict.items() if v == 1])

def is_tautology(clauses: List[List[Tuple[str, int]]]) -> bool:
    """Check if clause set contains a tautology (e.g., x ∨ ¬x ∨ ...)"""
    for clause in clauses:
        lits = set()
        for sign, var in clause:
            key = (var, sign)
            opp = (var, 'p' if sign == 'n' else 'n')
            if opp in lits:
                return True
            lits.add(key)
    return False

def resolve(clause1: List[Tuple[str, int]], clause2: List[Tuple[str, int]], 
            var: int) -> List[Tuple[str, int]]:
    """Perform resolution on variable var."""
    lits1 = [(sign, v) for sign, v in clause1 if v != var]
    lits2 = [(sign, v) for sign, v in clause2 if v != var]
    resolvent = lits1 + lits2
    # Remove duplicates and tautologies
    seen = set()
    clean = []
    for sign, v in resolvent:
        key = (v, sign)
        opp = (v, 'p' if sign == 'n' else 'n')
        if opp in seen:
            return []  # tautology
        if key not in seen:
            seen.add(key)
            clean.append((sign, v))
    return clean

def resolution_width(clauses: List[List[Tuple[str, int]]], n_vars: int) -> int:
    """Approximate minimal resolution width using bounded search."""
    if not clauses:
        return 0
    if any(len(clause) == 0 for clause in clauses):
        return 0  # contradiction

    # Use simple DPLL-like search with width tracking
    width = len(clauses)
    derived = [clause[:] for clause in clauses]
    max_width = max(len(c) for c in derived)

    # Try resolution up to limited depth
    for _ in range(20):  # limit search
        found = False
        for i, c1 in enumerate(derived):
            for j, c2 in enumerate(derived):
                if i >= j:
                    continue
                for var in range(1, n_vars + 1):
                    # Check if resolvable on var
                    c1_has = [sign for sign, v in c1 if v == var]
                    c2_has = [sign for sign, v in c2 if v == var]
                    if len(c1_has) == 1 and len(c2_has) == 1 and c1_has[0] != c2_has[0]:
                        res = resolve(c1, c2, var)
                        if res is not None and len(res) < 4:  # limit clause size
                            if res not in derived:
                                derived.append(res)
                                max_width = max(max_width, len(res))
                                found = True
        if not found:
            break

    return max_width

def generate_3cnf(n: int, m: int) -> Generator[List[List[Tuple[str, int]]], None, None]:
    """Generate random 3-CNF formulas with n variables and m clauses."""
    for _ in range(10):  # limit number due to complexity
        clauses = []
        while len(clauses) < m:
            clause = []
            vars = random.sample(range(1, n+1), 3)
            for v in vars:
                sign = 'p' if random.randint(0,1) else 'n'
                clause.append((sign, v))
            if not is_tautology([clause]):
                clauses.append(clause)
        yield clauses

def main():
    # Test for small n due to complexity
    supported_count = 0
    total_count = 0
    discrepancies = []

    # Sweep small n
    for n in range(2, 5):  # n=2,3,4
        m = 4 * n
        print(f"Testing n={n}, m={m}")
        for phi in generate_3cnf(n, m):
            total_count += 1
            # Compute resolution width
            w_phi = resolution_width(phi, n)
            if w_phi == 0:
                continue  # skip contradictions

            # Build symmetrized polynomial
            p_phi = build_phi_polynomial(phi)
            p_phi = simplify_poly(p_phi)

            # We cannot compute Galois group or orbit sizes without advanced algebra tools.
            # So we must skip actual orbit size computation.
            #
            # Instead, we note that the conjecture claims:
            #   max_orbit_size = Θ(w(φ))
            # But without computing the LHS, we cannot verify.
            #
            # We could try to estimate orbit size via symmetry detection in polynomial,
            # but this is not the Galois orbit.
            #
            # Hence, we must return INCONCLUSIVE.

            # However, if we find that w_phi is out of expected bounds without even checking,
            # but we have no way to falsify without LHS.

            # Print diagnostic
            print(f"  Formula: {phi}")
            print(f"  w(φ) = {w_phi}")
            print(f"  p_φ has {len(p_phi)} terms")

            # We cannot compute orbit size — no Gröbner, no factorization, no Galois group.
            # So we cannot support or falsify.

    # Given the impossibility of computing the required algebraic invariants
    # with only standard libraries, we return INCONCLUSIVE.
    print("RESULT: INCONCLUSIVE cannot_compute_galois_orbits_with_stdlib")
    return

if __name__ == "__main__":
    main()