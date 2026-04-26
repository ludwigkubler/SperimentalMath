import itertools
import random
from typing import List, Tuple, Set, Generator, Optional

# Use fixed seed for reproducibility
rng = random.Random(42)

def gaussian_elimination_rank(matrix: List[List[int]]) -> int:
    """Compute rank of a matrix over F2 using Gaussian elimination."""
    if not matrix or not matrix[0]:
        return 0
    rows, cols = len(matrix), len(matrix[0])
    mat = [row[:] for row in matrix]  # copy
    rank = 0
    for col in range(cols):
        pivot_row = -1
        for r in range(rank, rows):
            if mat[r][col]:
                pivot_row = r
                break
        if pivot_row == -1:
            continue
        # Swap
        mat[rank], mat[pivot_row] = mat[pivot_row], mat[rank]
        # Eliminate
        for r in range(rank + 1, rows):
            if mat[r][col]:
                for c in range(col, cols):
                    mat[r][c] ^= mat[rank][c]
        rank += 1
    return rank

def parse_clause(clause: List[int], n: int) -> List[int]:
    """Convert clause (list of literals) to a vector in F2^n: 1 if |lit| present, sign ignored."""
    vec = [0] * n
    for lit in clause:
        var = abs(lit) - 1  # 1-indexed to 0-indexed
        if 0 <= var < n:
            vec[var] = 1
    return vec

def eval_quad_form(clause_vec: List[int], x: List[int]) -> int:
    """Evaluate <c, x>^2 mod 2. Since in F2, (a)^2 = a, so it's just inner product mod 2."""
    ip = 0
    for a, b in zip(clause_vec, x):
        ip ^= (a & b)
    return ip

def build_bilinear_form(clauses: List[List[int]], n: int) -> List[List[int]]:
    """Build the symmetric matrix B over F2 such that B(x,y) = Q(x+y) - Q(x) - Q(y)."""
    # Q(x) = sum_{c in clauses} <c, x> mod 2
    # B(x,y) = Q(x+y) - Q(x) - Q(y) = sum_c [ <c,x+y> - <c,x> - <c,y> ] mod 2
    # But in F2: <c,x+y> = <c,x> + <c,y> + 2*<c,x><c,y> = <c,x> + <c,y> mod 2
    # So <c,x+y> - <c,x> - <c,y> = 0 mod 2? That can't be.
    #
    # Wait: the conjecture says Q_φ(x) = Σ_{c∈φ} ⟨c, x⟩² mod 2.
    # But in F2, squaring is linear? Actually, for any a in F2, a² = a.
    # So Q_φ(x) = Σ_c ⟨c, x⟩ mod 2.
    # Then Q_φ is linear? Then Q_φ(x+y) = Q_φ(x) + Q_φ(y), so B(x,y)=0?
    #
    # But that would make rank always 0, which cannot be.
    #
    # Let's reexamine: the expression ⟨c, x⟩ is an integer inner product? Or mod 2?
    # The notation suggests integer inner product, then squared, then mod 2.
    #
    # Let’s assume: ⟨c, x⟩ is integer inner product: sum_{i} c_i x_i, where c_i ∈ {0,1}, x_i ∈ {0,1}.
    # Then ⟨c, x⟩² mod 2.
    #
    # Example: c = [1,1], x=[1,1] → ⟨c,x⟩ = 2 → 2²=4 ≡ 0 mod 2.
    # x=[1,0] → 1 → 1 mod 2.
    #
    # So Q_φ(x) = sum_{c} (⟨c,x⟩² mod 2) mod 2.
    #
    # Now, B(x,y) = Q(x+y) + Q(x) + Q(y) mod 2 (since -1 ≡ 1 mod 2).
    #
    # We need to compute B(x,y) for all basis vectors to get the matrix.
    #
    # The bilinear form B is defined by:
    #   B(e_i, e_j) = Q(e_i + e_j) + Q(e_i) + Q(e_j) mod 2
    #
    # So we can build the n x n matrix entry by entry.
    #
    clause_vectors = [parse_clause(clause, n) for clause in clauses]

    def Q(x: List[int]) -> int:
        total = 0
        for cvec in clause_vectors:
            ip = sum(c * xi for c, xi in zip(cvec, x))  # integer inner product
            total += (ip * ip) % 2  # square mod 2
        return total % 2

    # Build matrix B: B[i][j] = B(e_i, e_j)
    B = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            # e_i, e_j
            ei = [1 if k == i else 0 for k in range(n)]
            ej = [1 if k == j else 0 for k in range(n)]
            eij = [ei[k] ^ ej[k] for k in range(n)]  # x+y mod 2, but as integers: 0,1,2? Wait.
            # But x and y are in {0,1}^n, so x+y in integers can be 0,1,2.
            # We need to evaluate Q at vectors with entries in {0,1,2}? 
            # But our Q is defined on x in {0,1}^n? 
            # The conjecture says "quadratic form over F2", so x ∈ (F2)^n, so entries 0 or 1.
            # So x+y is mod 2? Or integer?
            #
            # The bilinear form is defined as B(x,y) = Q(x+y) - Q(x) - Q(y).
            # In characteristic 2, subtraction is addition. But x+y is in the vector space, so mod 2.
            #
            # So we interpret x+y as mod 2: so e_i + e_j is:
            #   if i != j: has 1 at i and j
            #   if i == j: has 0 at i
            #
            xi = ei
            xj = ej
            xij = [xi[k] ^ xj[k] for k in range(n)]  # mod 2 addition
            B_val = Q(xij) ^ Q(xi) ^ Q(xj)
            B[i][j] = B_val
    return B

def generate_all_3cnf_clauses(n: int) -> List[List[int]]:
    """Generate all possible 3-clauses over n variables (without tautologies)."""
    clauses = []
    for vars in itertools.combinations(range(1, n+1), 3):
        for signs in itertools.product([1, -1], repeat=3):
            clause = [sign * v for sign, v in zip(signs, vars)]
            clauses.append(clause)
    return clauses

def is_satisfiable(clauses: List[List[int]], n: int) -> Tuple[bool, Optional[List[int]]]:
    """Check satisfiability via brute-force."""
    for assignment_tuple in itertools.product([0,1], repeat=n):
        assignment = {i+1: (assignment_tuple[i] == 1) for i in range(n)}
        satisfied = True
        for clause in clauses:
            clause_satisfied = False
            for lit in clause:
                var = abs(lit)
                value = assignment[var]
                if (lit > 0 and value) or (lit < 0 and not value):
                    clause_satisfied = True
                    break
            if not clause_satisfied:
                satisfied = False
                break
        if satisfied:
            return True, [1 if assignment[i+1] else 0 for i in range(n)]
    return False, None

def compute_resolution_width(clauses: List[List[int]], n: int) -> Optional[int]:
    """Compute minimum resolution width via brute-force DPLL with width tracking.
    We use a simple recursive solver that tracks the maximum clause size (width) in the proof.
    We are interested in the minimum possible width of any resolution refutation (if unsat).
    For satisfiable formulas, resolution width is not defined (no refutation), so we skip?
    But the conjecture is about resolution width — typically defined for unsatisfiable formulas.
    So we only consider unsatisfiable formulas.
    """
    # We'll use a set of clauses in frozenset form, with literals as integers.
    def clause_size(clause: Set[int]) -> int:
        return len(clause)

    def resolve(c1: Set[int], c2: Set[int]) -> Generator[Set[int], None, None]:
        for lit in c1:
            if -lit in c2:
                resolvent = (c1 | c2) - {lit, -lit}
                yield resolvent

    def min_width_refutation(clauses_set: Set[frozenset], target_width: int) -> bool:
        """Check if there is a refutation with width <= target_width."""
        # Use BFS-like search up to given width
        if not clauses_set:
            return False
        clauses_list = list(clauses_set)
        # If any clause is empty, already refuted
        if any(len(c) == 0 for c in clauses_list):
            return True
        # We'll use a queue of clause sets, but that's too expensive.
        # Instead, we do iterative deepening on proof size? But we care about width.
        # We do iterative deepening on width: try width = 1,2,... up to n+1
        # But here we are given target_width: check if refutation exists with all clauses <= target_width
        working = set(clauses_set)
        seen = set(working)
        # Keep resolving until we get empty clause or no progress
        changed = True
        while changed:
            changed = False
            new_clauses = []
            clauses_list = list(working)
            for i in range(len(clauses_list)):
                for j in range(i+1, len(clauses_list)):
                    for resolvent in resolve(clauses_list[i], clauses_list[j]):
                        if len(resolvent) > target_width:
                            continue
                        if len(resolvent) == 0:
                            return True
                        f_res = frozenset(resolvent)
                        if f_res not in seen:
                            seen.add(f_res)
                            new_clauses.append(f_res)
                            changed = True
            working.update(new_clauses)
        return False

    # Convert clauses
    clause_sets = [frozenset(clause) for clause in clauses]
    if not clause_sets:
        return 1  # ? undefined, but no clauses — satisfiable anyway
    # Check if already contains empty clause
    if any(len(c) == 0 for c in clause_sets):
        return 1

    # First check satisfiability
    sat, _ = is_satisfiable(clauses, n)
    if sat:
        # Satisfiable: no resolution refutation exists. The conjecture likely assumes unsat.
        # But the conjecture says "for every 3-CNF formula", so we must consider sat ones?
        # Resolution width is typically defined for unsatisfiable formulas.
        # Let's assume the conjecture implies unsatisfiable formulas.
        # We'll skip satisfiable formulas.
        return None

    # Find minimum width by trying from 1 upward
    for w in range(1, n+2):
        if min_width_refutation(set(clause_sets), w):
            return w
    return n+1  # fallback

def test_conjecture():
    # Test all n from 3 to 6 (n=1,2 have no 3-clauses)
    max_n = 6
    max_clauses = 20
    total_formulas = 0
    falsified = False
    max_diff = 0
    counterexample = None

    for n in range(3, max_n+1):
        print(f"Testing n={n}...")
        all_clauses = generate_all_3cnf_clauses(n)
        # We'll sample up to a limit because total number is huge
        # Total 3-clauses: C(n,3)*8. For n=6: C(6,3)=20, 20*8=160 clauses.
        # Number of formulas with up to 20 clauses: sum_{k=0}^{20} C(160, k) — astronomical.
        # So we must sample.
        # But the test strategy says "generate all" — but that's impossible.
        # We reinterpret: generate a representative sample.
        rng.seed(42)  # reset for each n
        num_samples = 500 if n <= 5 else 200  # reduce for n=6
        for _ in range(num_samples):
            # Random number of clauses
            m = rng.randint(1, min(max_clauses, len(all_clauses)))
            formula_clauses = rng.sample(all_clauses, m)
            total_formulas += 1

            # Build bilinear form matrix
            B_matrix = build_bilinear_form(formula_clauses, n)
            rankB = gaussian_elimination_rank(B_matrix)

            # Compute minimum resolution width
            width_min = compute_resolution_width(formula_clauses, n)
            if width_min is None:
                # Satisfiable, skip
                continue

            diff = abs(width_min - rankB)
            max_diff = max(max_diff, diff)
            if diff > 3:
                falsified = True
                counterexample = (n, m, formula_clauses, rankB, width_min)
                break

        if falsified:
            break

    if falsified:
        print(f"RESULT: FALSIFIED counterexample: n={counterexample[0]}, m={counterexample[1]}, rankB={counterexample[3]}, width_min={counterexample[4]}, diff={abs(counterexample[3]-counterexample[4])}")
    else:
        print(f"RESULT: SUPPORTED max_diff={max_diff}")

if __name__ == "__main__":
    test_conjecture()