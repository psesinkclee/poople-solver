# poople-solver

A Python solver for the daily word game [Poople](https://poople.io) that finds all optimal paths from a given starting word to POOP.

## What is Poople?

Poople is a daily word game where you're given a 4-letter starting word and must reach the word POOP by changing one letter at a time, with every step being a valid word.

## How it works

The solver fetches the word bank directly from Poople's source, which includes each word's precomputed Hamming distance to POOP. It uses this to perform a greedy descent through the word graph, enumerating every optimal path from the starting word to POOP.

If a local `poopbank.txt` cache exists in the script directory, it will be used instead of fetching from the web. Delete the file to force a fresh fetch.

## Notes

- The word bank is scraped directly from Poople.io's JS bundle and cached locally as `poopbank.txt`
- The asset filename in the bundle is detected dynamically, so the solver should survive site redeployments
- `poopbank.txt` is excluded from version control and it will be generated on first run
