# poople-solver

A Python solver for the daily word game [Poople](https://poople.io) that finds all optimal paths from a given starting word to POOP.

## What is Poople?

Poople is a daily word game where you're given a 4-letter starting word and must reach the word POOP by changing one letter at a time, with every step being a valid word.

## How it works

The solver fetches the word bank directly from Poople's JS bundle, which includes each word's precomputed breadth-first search (BFS) distance to POOP. This distance represents the minimum number of single-letter substitutions required to reach POOP through valid words only.
Rather than running pathfinding at query time, the solver exploits these precomputed distances to perform a greedy descent through the word graph. Starting from the input word at distance N, it finds all adjacent words (Hamming distance = 1) at distance N-1, recurses into each, and collects every path that terminates at POOP. This guarantees all returned paths are optimal (perfect score).

Where multiple neighbors exist at the next distance level, all branches are explored, so the solver returns every optimal path rather than just one.

If a local `poopbank.txt` cache exists in the script directory, it will be used instead of fetching from the web. Delete the file to force a fresh fetch.

## Notes

- The word bank is scraped directly from Poople.io's JS bundle and cached locally as `poopbank.txt`
- The asset filename in the bundle is detected dynamically, so the solver should survive site redeployments
- `poopbank.txt` is excluded from version control and it will be generated on first run
