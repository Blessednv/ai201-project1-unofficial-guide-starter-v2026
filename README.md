# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** No fixed size — each chunk is one `##` section of a guide, so
length is set by the document, not by a number. In practice this gives
174–762 characters, averaging 322.

**Overlap:** None. Sections don't bleed into each other, so there is nothing
to overlap. The one thing deliberately repeated across chunks is the document
title.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

I picked `city_guides`, which is fourteen long travel guides averaging about
2,000 characters each. Every guide is already written as labelled sections —
`## Getting there`, `## Eat and drink`, `## When to go` — and each section is
one self-contained topic. The starter's chunker ignored all of that and cut
every 800 characters instead.

Reading the starter's output showed what that cost. Of 51 chunks, 35 began
mid-word or mid-sentence. In `guide_eating.md` the cut landed inside the
heading `## Opening hours`, leaving one chunk ending `"## Opening ho"` and the
next beginning `"urs"` — so the chunk holding the answer no longer said
anywhere that it was about opening hours. The shortest chunk was 24 characters
(`"d Sundays and after 5pm."`), the leftover tail of a document that didn't
divide evenly.

So I split on the `##` headings instead, letting the structure decide where
chunks end.

That alone wasn't enough. All nine town guides use the same seven section
labels, so a chunk reading `## Eat and drink / Four pubs, two cafés...` never
said which town it came from — and the search only reads the chunk's text; the
filename is stored separately and isn't searched. I fixed that by pasting the
document's title onto every chunk, so each one names both the place and the
topic. It acts as an anchor.

I also dropped the character cap entirely rather than keeping 800 as a safety
limit. A limit would just reintroduce the problem: an 805-character section
would get sliced at 800 and lose its last sentence. The real ceiling is the
embedding model, which truncates at 256 tokens — my longest chunk is 162
tokens, so there is room to spare and no reason to cut on length at all.

Result: 94 chunks instead of 51, averaging 322 characters, shortest 174
instead of 24, and none starting mid-word.

One thing I'd flag honestly: keeping the introduction paragraphs produced one
chunk that is pure preamble (`guide_accessibility.md#0` — "An honest
assessment rather than a promotional one") and answers no question on its own.
I checked whether it crowds out real answers by searching "which towns are
hardest to get around with a wheelchair" — it didn't reach the top five,
because it has no specific content to match against. I left it in rather than
adding code to remove it.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
# Corry Vale

## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
# Givens Mill

## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
# Kestrelford

## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
# Pellew Sands

## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** How long does it take to drive the coast road to Halden Bay?

**Answer:**

```
(best distance 0.198, cutoff 0.6)

======================================================================
System instruction sent with the prompt
======================================================================
You answer questions using only the documents provided to you.

Rules:
1. Use only the information in the documents below. Do not use anything you know from elsewhere.
2. If the documents don't cover the question, say you don't have enough information. Do not guess.
3. Name the document your answer came from, using the filename given in each excerpt.
4. Be brief. Two or three sentences is usually enough.
5. If a document mentions more than one relevant detail (for example, two
   different date ranges or options), only report the one that actually
   answers the question asked, not all of them.

======================================================================
The assembled prompt, exactly as sent
======================================================================
Documents:

[from guide_halden_bay.md]
# Halden Bay

## Getting there

The coast road is the only approach and it is slow — 40 minutes for 22 miles, with the last stretch cut into the cliff. Buses run four times a day. Parking in the town itself is limited to two small lots that fill by 10am on summer weekends; the overflow lot is a 12-minute walk up a hill.

[from guide_regional_transport.md]
# Getting around the region

## Driving

Roads are good between the towns and poor on the approaches to both Kestrelford
and Halden Bay. The Kestrelford approach is single-track with passing places
for the final eight minutes. The Halden Bay coast road is cut into the cliff
and is slow rather than difficult.

Parking is the constraint rather than driving. Both Halden Bay lots fill by
10am on summer weekends. Kestrelford's lower car park is free and involves a
steep walk up.

[from guide_halden_bay.md]
# Halden Bay

## What to see

The harbour at 6am when the boats come in is the thing worth setting an alarm for. The coastal path runs in both directions, north to a lighthouse in about two hours and south along the cliffs for as far as you want. The small museum on Fell Street covers the fishing industry and takes 40 minutes.

[from guide_halden_bay.md]
# Halden Bay

## Getting around

The town is small enough to cross in fifteen minutes but is built on three levels connected by stepped lanes, which makes it hard going with luggage or a pushchair. The harbour front is level; everything above it is not.

[from guide_walking.md]
# Walking in the region

## Serious, and weather-dependent

The **Halden Bay coastal path** runs north to a lighthouse in about two hours
and south along the cliffs indefinitely. It is exposed, and it is closed in high
wind — this is enforced and the closures are not advisory.

The **Elder Ness shingle** walk to the lighthouse is only 25 minutes but shingle
is much harder going than the distance suggests. The single access road to the
headland floods at the highest spring tides, about six times a year, for roughly
two hours either side of high water.

---

Question: How long does it take to drive the coast road to Halden Bay?

Answer using only the documents above, and name the file you used.
======================================================================

It takes 40 minutes to drive the coast road to Halden Bay (from `guide_halden_bay.md`).

Sources retrieved: guide_halden_bay.md, guide_regional_transport.md, guide_walking.md

1 model calls this session, 716 tokens (689 in, 27 out)
```

**My relevance cutoff:**

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

I kept the starter's default of **0.6**. I ran my five test questions and the
five `OUT_OF_SCOPE` questions and measured the best distance for each. My
worst in-corpus question scored 0.295 and my closest out-of-scope question
scored 0.803 — a gap of about 0.5 with nothing in it. 0.6 sits roughly in the
middle of that gap, giving about 0.3 of slack on either side, so I saw no
reason to move it away from the default.

| Question | In corpus? | Best distance |
|---|---|---|
| How long does it take to drive the coast road to Halden Bay? | Yes | 0.198 |
| How often do the trams run in Marchwood on weekdays? | Yes | 0.236 |
| What time does the farm shop at the mouth of Corry Vale close? | Yes | 0.285 |
| What are the best two months to visit Elder Ness if I want to see the spring bird migration? | Yes | 0.288 |
| Does Kestrelford have good public transportation within the town itself? | Yes | 0.295 |
| What is the capital of Mongolia? | No | 0.803 |
| What is the recommended dosage of ibuprofen for a headache? | No | 0.835 |
| How do I write a for loop in Rust? | No | 0.836 |
| How do I change the oil in a diesel engine? | No | 0.888 |
| Who won the 1994 World Cup? | No | 0.975 |

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.** I wrote a draft of the chunking function and asked Claude to review it
against its own draft. Both produced byte-identical output on `city_guides`
(94 chunks), so I tested them on edge cases instead. On a one-line document
with no heading, Claude's version silently deleted the document and mine kept
it — mine checked `lines[0].startswith('# ')` before treating the first line
as a title, and Claude's just assumed the first line was one. A second AI tool
told me to use Claude's version and described that exact line as
"mathematically foolproof"; the test showed it wasn't. The version I shipped
takes the regex look-ahead split from Claude's draft, because it keeps the
`##` heading attached instead of deleting and re-gluing it, and the title
guard from mine.

**2.** I wrote my five acceptance criteria and asked Claude to fact-check the
reasoning rather than write it. Two of my stated reasons turned out to
describe things that weren't in my test set: I justified criterion 1 using
`guide_eating.md`, which none of my five questions actually touch, and
justified criterion 3 with a hospital question that isn't in my `OUT_OF_SCOPE`
list. Claude then suggested adding that hospital question to make the
criterion harder — and measuring it disproved the suggestion, since it scored
0.326 against a 0.6 threshold, meaning my corpus genuinely answers it and it
isn't out-of-scope at all. I rewrote criterion 1's reason around duplicated
facts that are in my real questions, and raised criterion 3 from 4 of 5 to
5 of 5.

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
