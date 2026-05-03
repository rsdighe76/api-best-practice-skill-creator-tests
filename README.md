# API Best Practice Skill Creator — Tests

Test fixtures and eval checklist for [api-best-practice-skill-creator](https://github.com/rsdighe76/claude-skills).

## Structure

```
api-best-practice-skill-creator-tests/
  fixtures/
    acme-orders-openapi.yaml    test spec (ACME Orders API, 8 endpoints)
  test-output/                  generated skill lands here (gitignored)
  eval-checklist.md             what correct output looks like
```

## Running a test

1. Open Claude Code in this directory (or any directory)
2. Run `/api-best-practice-skill-creator`
3. When prompted for a spec, provide: `../api-best-practice-skill-creator-tests/fixtures/acme-orders-openapi.yaml`
4. When prompted for output path, use: `../api-best-practice-skill-creator-tests/test-output/`
5. Check generated files against `eval-checklist.md`

## Eval scoring

Open `eval-checklist.md` and tick off each item against the files in `test-output/`.
Target is 100% before distributing the skill.
