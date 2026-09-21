# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
I picked 4 of 5 because two of my facts are duplicated across documents — the
Marchwood tram frequency (8 minutes) appears in both `guide_marchwood.md` and
`guide_accessibility.md`, and the Kestrelford transport fact appears in both
`guide_kestrelford.md` and `guide_accessibility.md`. I expect retrieval might
occasionally surface the less-detailed duplicate instead of the primary
source, so I want room for one miss without treating it as a broken pipeline.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
I picked 5 of 5 because this is purely a formatting instruction in the system
prompt. The model either reliably follows the instruction to cite its source
every single time, or the prompt design is flawed. There is no acceptable
reason for it to skip a citation.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 5 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
I picked 5 of 5 because my five out-of-scope questions (capital of Mongolia,
diesel oil changes, the 1994 World Cup, ibuprofen dosage, Rust for-loops)
share no vocabulary or topic overlap with a UK-style travel-guide corpus at
all. There's no plausible reason for any of them to land close enough to pass
the gate, so this is a case where the target should be the strictest one
rather than a hedge.

---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->

When I run `python app.py chunks -n 5` to pull 5 chunks spread evenly across
my index, at least 4 of those 5 will begin at the start of a new sentence or
Markdown heading, rather than cutting into the middle of a word or phrase.

**Why this target:**
The `city_guides` corpus is structured with very short, specific paragraphs
under clear Markdown headings (like `## Eat and drink`). A successful
chunking strategy for this data should respect these natural paragraph breaks
instead of blindly slicing text exactly at an arbitrary character limit.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

In 5 out of 5 of my test questions, the final generated answer will not
invent or hallucinate any town names, prices, or operating hours that are
missing from the explicitly retrieved source chunks.

**Why this target:**
I picked 5 of 5 because travel advice requires absolute factual accuracy.
Hallucinating that a train runs at a certain time or that a pub is open when
it isn't would ruin a trip. The model must strictly ground its facts in the
documents 100% of the time, with no exceptions.



---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
