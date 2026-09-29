import assert from 'node:assert/strict'
import {mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync} from 'node:fs'
import {tmpdir} from 'node:os'
import {join} from 'node:path'
import test from 'node:test'
import {check} from '../scripts/check_workflow_docs.mjs'

function fixture(status = 'Ready') {
  const root = mkdtempSync(join(tmpdir(), 'workflow-check-'))
  const put = (path, text) => {
    const file = join(root, path)
    mkdirSync(join(file, '..'), {recursive: true})
    writeFileSync(file, text)
  }
  put('.workflow/backlog.md', '# Backlog\n\n## B-0001: First\n\n- Feature Brief: [First](features/B-0001/brief.md).\n')
  put('.workflow/context.md', '# Context\n\n## Job reservation\n\nA saved resource.\n')
  put('.workflow/features/B-0001/brief.md', `# First

Status: ${status}
Feature ID: B-0001

## Goal

Give the user a result.

## Stories and acceptance

### S1: First story

Story: A user acts and sees the result.

Acceptance:

- The user sees the result.

## Scope

The first result.

## Non-goals

The second result.

## Related records

- [Job reservation](../../context.md#job-reservation).
`)
  return {root, put, cleanup: () => rmSync(root, {recursive: true, force: true})}
}

test('valid Ready brief and canonical backlog link pass', async () => {
  const sample = fixture()
  try { assert.deepEqual(await check(sample.root), []) }
  finally { sample.cleanup() }
})

test('Draft omissions warn and Ready omissions fail', async () => {
  for (const status of ['Draft', 'Ready']) {
    const sample = fixture(status)
    try {
      sample.put('.workflow/features/B-0001/brief.md', `# First

Status: ${status}
Feature ID: B-0001

## Goal

## Stories and acceptance

### S1: One

### S3: Three

Story: A user acts.

Acceptance:

## Scope

## Non-goals
`)
      const findings = await check(sample.root)
      for (const code of ['FB005', 'FB007', 'FB008', 'FB009', 'FB010']) {
        assert.ok(findings.some(item => item.code === code), code)
      }
      assert.ok(findings.every(item => item.warning === (status === 'Draft')))
    } finally { sample.cleanup() }
  }
})

test('structural failures stay errors in Draft', async () => {
  const sample = fixture('Draft')
  try {
    sample.put('.workflow/features/B-0001/brief.md', `# First

Status: Draft
Feature ID: B-0002

## Goal

Some goal.

## Goal

Another goal.

## Stories and acceptance

### S1: One

Story: A user acts.

Acceptance:

- A result.

### S1: Two

Story: A user acts.

Acceptance:

- A result.

## Scope

Some scope.

## Non-goals

Some boundary.

## Related records

- [Missing](../../context.md#job-reservaton).
`)
    const findings = await check(sample.root)
    for (const code of ['FB003', 'FB004', 'FB006', 'LINK002']) {
      assert.ok(findings.some(item => item.code === code && !item.warning), code)
    }
  } finally { sample.cleanup() }
})

test('duplicate labels on soft lines are structural errors', async () => {
  const sample = fixture('Draft')
  try {
    const path = '.workflow/features/B-0001/brief.md'
    let source = readFileSync(join(sample.root, path), 'utf8')
    source = source.replace('Story: A user acts and sees the result.',
      'Story: A user acts.\nStory: The user sees a result.')
    source = source.replace('Acceptance:\n', 'Acceptance:\nAcceptance:\n')
    sample.put(path, source)
    const findings = await check(sample.root)
    assert.ok(findings.some(item => item.code === 'FB008' && !item.warning))
    assert.ok(findings.some(item => item.code === 'FB009' && !item.warning))
  } finally { sample.cleanup() }
})

test('backlog identity and canonical backlink are checked', async () => {
  const sample = fixture('Draft')
  try {
    sample.put('.workflow/backlog.md', `# Backlog

## B-0001: First

- Feature Brief: [Wrong](features/B-0002/brief.md).

## B-0001: Duplicate

- Feature Brief: [First](features/B-0001/brief.md).
`)
    const findings = await check(sample.root)
    assert.ok(findings.some(item => item.code === 'FB013'))
    assert.ok(findings.some(item => item.code === 'FB014'))
    assert.ok(findings.some(item => item.code === 'LINK001'))
  } finally { sample.cleanup() }
})

test('legacy Source brief link counts as a backlink', async () => {
  const sample = fixture()
  try {
    sample.put('.workflow/backlog.md', '# Backlog\n\n## B-0001: First\n\n- Source: [First](features/B-0001/brief.md).\n')
    assert.deepEqual(await check(sample.root), [])
  } finally { sample.cleanup() }
})

test('a resolved canonical path can include a dot segment', async () => {
  const sample = fixture()
  try {
    sample.put('.workflow/backlog.md', '# Backlog\n\n## B-0001: First\n\n' +
      '- Feature Brief: [First](./features/B-0001/brief.md).\n')
    assert.deepEqual(await check(sample.root), [])
  } finally { sample.cleanup() }
})

test('word limits retain source whitespace counting', async () => {
  const sample = fixture()
  try {
    sample.put('.workflow/direction.md', 'word '.repeat(4001))
    sample.put('.workflow/decisions/pdr/0001-choice.md', 'word '.repeat(501))
    const findings = await check(sample.root)
    assert.equal(findings.filter(item => item.code === 'SIZE001').length, 2)
  } finally { sample.cleanup() }
})

test('Feature Brief hard limit is still 1000 source words', async () => {
  const sample = fixture()
  try {
    const path = '.workflow/features/B-0001/brief.md'
    const source = readFileSync(join(sample.root, path), 'utf8')
    sample.put(path, source + '\n' + 'word '.repeat(1000))
    assert.ok((await check(sample.root)).some(item => item.code === 'SIZE001' &&
      item.message.includes('Feature Brief')))
  } finally { sample.cleanup() }
})

test('an optional section is optional but cannot be empty in Ready', async () => {
  const sample = fixture()
  try {
    const path = '.workflow/features/B-0001/brief.md'
    const source = '# First\n\nStatus: Ready\nFeature ID: B-0001\n\n' +
      '## Goal\n\nA result.\n\n## Stories and acceptance\n\n' +
      '### S1: Act\n\nStory: A user acts.\n\nAcceptance:\n\n' +
      '- The user sees a result.\n\n## Feature-wide constraints and acceptance\n\n' +
      '## Scope\n\nA result.\n\n## Non-goals\n\nOther results.\n'
    sample.put(path, source)
    const findings = await check(sample.root)
    assert.ok(findings.some(item => item.code === 'FB005' &&
      item.message.includes('Feature-wide constraints') && !item.warning))
    sample.put(path, source.replace('## Feature-wide constraints and acceptance\n\n', ''))
    assert.deepEqual(await check(sample.root), [])
  } finally { sample.cleanup() }
})

test('a wrong backlink fails even when that backlog item has no brief', async () => {
  const sample = fixture()
  try {
    sample.put('.workflow/backlog.md', `# Backlog

## B-0001: First

- Feature Brief: [First](features/B-0001/brief.md).

## B-0002: Second

- Feature Brief: [Wrong](features/B-0001/brief.md).
`)
    const findings = await check(sample.root)
    assert.ok(findings.some(item => item.code === 'FB013' &&
      item.message.includes('B-0002')))
    assert.deepEqual(findings, await check(sample.root))
  } finally { sample.cleanup() }
})

test('generic Markdown lint applies to workflow files', async () => {
  const sample = fixture()
  try {
    sample.put('.workflow/extra.md', '# Root\n\n### Skipped level\n\nText.\n')
    const findings = await check(sample.root)
    assert.ok(findings.some(item => item.code === 'MD001' &&
      item.path === '.workflow/extra.md'))
  } finally { sample.cleanup() }
})
