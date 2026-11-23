# Mathar's half-factorial recurrence conjectures: extensions of Jovovic's formulas and Barry's array sums

Haobo Ma — ChronoAI Pte Ltd, Singapore  
Wenlin Zhang — National University of Singapore; ChronoAI Pte Ltd, Singapore

The note proves Mathar's recurrence conjectures in OEIS A081124 (Formula,
24 November 2012, posing revision 8, retained in revision 20) and A084261
(Formula, 30 November 2012, posing revision 9, retained in revision 29),
for every integer n ≥ 3. The finite-sum proofs are
complemented by extensions of Jovovic's generating functions.

The weighted factorial transform c_n(t) has an explicit recurrence,
ordinary continued fraction and parameter-independent Hankel determinants.
The note proves the formulas attributed to Hanna and Barry in A084261,
A161556 and A137704. It also proves the linked A081123/A081125 product,
factorial-ratio and reciprocal-sum identities. One A081125 interval product
is corrected: at n=2 the recorded product is 1, whereas n!/floor(n/2)! is 2;
the correct product runs from floor(n/2)+1 through n.
The equivalent SageMath expression is corrected to
`rising_factorial(floor(n/2)+1,ceil(n/2))`.

Earlier counting interpretations are credited to Goyt–Pudwell (2012) and
Fang–Hamaker–Troyka (2020/2022). Barry's 2009 thesis, Section 13.2,
pages 283–284, already establishes the array-sum identity; its Example 64,
pages 53–54, gives the t=2 continued fraction. These identities are
reproved with attribution. No priority claim is made.

## Building

`note.tex` is the sole main source. Its bibliography is embedded; there are
no external figures, bibliography files or LaTeX inputs.

Use Tectonic 0.17.0:

```sh
tectonic note.tex
```

Alternatively run `pdflatex note.tex` twice. Shell escape and Python
packages are not needed to build the PDF.

## Mathematical coverage

`coverage.json` maps source statements to their exact locators and written
proofs. The pinned Lean declaration
`D5.S1.Recurrence.MatharA081124.result` proves the A081124 recurrence for the
inclusive binomial sum in the integers, for all natural n ≥ 3:

https://github.com/the-omega-institute/trureturing/blob/13f4288c2940bd2aa4020cec789956b9265769f5/D5/S1/Recurrence/MatharA081124.lean

The second pinned Lean declaration,
`D5.S1.Recurrence.MatharA084261.result`, proves the A084261 recurrence for
the inclusive even-index binomial sum in the integers, for every natural n ≥ 3:

https://github.com/the-omega-institute/trureturing/blob/50af3c7111e85c1112ee9dbc6e721adbb759a26b/D5/S1/Recurrence/MatharA084261.lean

The transfer lemma, generating functions, weighted
identities, continued fractions, Hankel determinants and linked factorial
identities have written proofs in the note. The scripts supply finite
exact-arithmetic checks, not replacements for the all-index proofs.
Asymptotics and the A081123/A081125 continued fractions are not covered.

## Exact finite checks

Use Python 3.10 or later; both scripts use only its standard library:

```sh
python3 verify.py --output checks.json
python3 verify-siblings.py --output checks-siblings.json
```

- Defining sums and recurrence-generated terms: indices 0–256.
- Parity identities: indices 0–512.
- Pascal/weighted identities, EGF coefficients and partial sums: indices
  or degrees 0–64; both 28-term OEIS prefixes are also compared.
- Weighted recurrence, partial sums, A161556 row polynomials and continued
  fractions: indices or degrees 0–64 for t = -2, -1, 0, 1/2, 1, 2.
- Hankel determinant products: determinant indices 0–12 at those six values.
- Both shorter inhomogeneous recurrences: indices 2–128.
- Somos array formula, symmetry, boundary values and recurrence: both
  coordinates 0–48; its antidiagonal sums: indices 0–48.
- Linked factorial-ratio EGF coefficients, corrected products and swinging
  identities: indices 0–512; companion recurrence: indices 3–512.
- The erroneous source interval product is checked explicitly at n=2.

`checks.json` and `checks-siblings.json` contain the deterministic expected
outputs, including each script's SHA256. All calculations use integers and
exact rational numbers. The convergent reciprocal sums and gamma identities
have the written analytic proofs in the note.

## Files and license

`metadata.json` contains the title, creators, license and the two established
problem identifiers. Additional linked identities have source coverage rows
without new problem identifiers. `SHA256SUMS` lists hashes of the scientific
source files; the PDF is distributed separately from the source archive.

Copyright © 2026 Haobo Ma and Wenlin Zhang. The note, its source and code are
licensed under Creative Commons Attribution 4.0 International (CC BY 4.0):
https://creativecommons.org/licenses/by/4.0/.
Sequence data in `reference-values.json` are attributed to the OEIS
Foundation; their source terms are https://oeis.org/LICENSE.
