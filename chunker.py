"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

import re
from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split documents into chunks. ⚠️ REPLACE THE BODY OF THIS IN MILESTONE 3.

    Right now it just calls the fallback. That is the plain, generic behaviour
    the brief is talking about.

    When you write your own strategy, set `produced_by` to
    "chunker.py::split_documents" so your README's Sample Chunks section names
    the right function. `app.py chunks` prints that string for you.

    Things worth thinking about before you write any code:
      - Are your documents short posts or long guides?
      - Is the useful information in one sentence, or spread over a paragraph?
      - Would splitting on paragraph breaks keep more thoughts intact than
        splitting on a character count?

    ── MILESTONE 3: what this now does, in plain English ─────────────────────

    THE IDEA
    Every guide in this corpus is already written as labelled sections —
    "## Getting there", "## Eat and drink", "## When to go" — and each one is
    a self-contained topic. So instead of counting to 800 characters and
    cutting wherever we land, we cut at the labels.

    THE CATCH
    All nine town guides use the SAME labels. A chunk reading "## Eat and
    drink / Four pubs, two cafes..." never says WHICH town it came from, and
    the search only ever reads the chunk's own text — the filename is stored
    separately and is not searched.

    THE FIX
    Paste the document's title ("# Kestrelford") on top of every chunk, so
    each one names both the place and the topic and stands on its own.
    """
    chunks: list[Chunk] = []

    for doc in documents:

        # STEP 1 — Cut the document into blocks, one per "## " heading.
        #
        # "\n(?=## )" means: cut at a line break that is FOLLOWED BY "## ".
        # The "(?=...)" is a look-ahead: it checks the heading is there but
        # does not eat it. So each block keeps its own heading on top,
        # instead of the heading being swallowed by the cut.
        blocks = re.split(r"\n(?=## )", doc.text)

        # STEP 2 — Find the document's title, e.g. "# Kestrelford".
        #
        # We only treat the first line as a title if it really starts with
        # "# ". Without this check, a document that has no title at all
        # would have its first sentence mistaken for one.
        first_line = blocks[0].strip().split("\n")[0]
        title = first_line if first_line.startswith("# ") else ""

        index = 0

        # STEP 3 — Turn each block into a chunk.
        for position, block in enumerate(blocks):
            block = block.strip()

            if position == 0:
                # The opening block. If it is nothing but the title, there
                # is no information in it, so we skip it. Otherwise it is
                # an introduction paragraph and we keep it as it is — it
                # already has the title on top.
                if block == title:
                    continue
                text = block
            else:
                # A normal "## " section. Paste the title above it so the
                # chunk says which town it is about. (If the document had
                # no title, leave the section as it is.)
                text = f"{title}\n\n{block}" if title else block

            # STEP 4 — Store the finished chunk.
            chunks.append(
                Chunk(
                    text=text,
                    source=doc.source,
                    index=index,
                    produced_by="chunker.py::split_documents",
                )
            )
            index += 1

    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
