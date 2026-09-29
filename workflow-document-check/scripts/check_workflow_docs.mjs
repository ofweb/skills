#!/usr/bin/env node
import {existsSync, readFileSync, readdirSync, statSync} from 'node:fs'
import {dirname, join, relative, resolve, sep} from 'node:path'
import {fileURLToPath} from 'node:url'
import {remark} from 'remark'
import remarkGfm from 'remark-gfm'
import {engine} from 'unified-engine'
import config from '../remark.config.mjs'

const here = dirname(fileURLToPath(import.meta.url))
const skill = resolve(here, '..')
const parser = remark().use(remarkGfm)
const limits = {
  direction: 4000, direction_topic: 2000, backlog: 1800, backlog_item: 80,
  context: 1500, context_entry: 80, feature_brief: 1000,
  acceptance_report: 800, pdr: 500, adr: 700
}
const required = ['Goal', 'Stories and acceptance', 'Scope', 'Non-goals']
const namedSections = new Set([...required, 'Feature-wide constraints and acceptance',
  'Related records', 'Open questions and assumptions'])
const featurePattern = /^B-\d{4}$/
const storyPattern = /^S([1-9]\d*):\s+\S/

function words(value) {
  return value.trim() ? value.trim().split(/\s+/u).length : 0
}

function nodeText(node) {
  if (typeof node.value === 'string') return node.value
  return (node.children || []).map(nodeText).join('')
}

function pathName(root, file) {
  return relative(root, file).split(sep).join('/')
}

function compare(left, right) {
  return left < right ? -1 : left > right ? 1 : 0
}

function walk(folder, predicate = () => true) {
  if (!existsSync(folder)) return []
  const files = []
  for (const entry of readdirSync(folder, {withFileTypes: true}).sort((a, b) => compare(a.name, b.name))) {
    if (entry.name === '.git' || entry.name === 'node_modules') continue
    const path = join(folder, entry.name)
    if (entry.isDirectory()) files.push(...walk(path, predicate))
    else if (entry.isFile() && predicate(path)) files.push(path)
  }
  return files
}

function issue(issues, code, path, line, message, warning = false) {
  issues.push({code, path, line, message, warning})
}

function document(root, file) {
  const source = readFileSync(file, 'utf8')
  return {file, path: pathName(root, file), source, tree: parser.parse(source)}
}

function sections(doc) {
  const result = []
  let current
  for (const node of doc.tree.children) {
    if (node.type === 'heading' && node.depth === 2) {
      current = {name: nodeText(node), heading: node, nodes: []}
      result.push(current)
    } else if (current) {
      current.nodes.push(node)
    }
  }
  return result
}

function sectionWords(doc, section, next) {
  const lines = doc.source.split(/\r?\n/u)
  const start = section.heading.position.start.line - 1
  const end = next ? next.heading.position.start.line - 1 : lines.length
  return words(lines.slice(start, end).join('\n'))
}

function validateSize(doc, issues, limit, label) {
  const count = words(doc.source)
  if (count > limit) issue(issues, 'SIZE001', doc.path, 1,
    `${label} has ${count} words; hard limit ${limit}`)
}

function validateRecords(doc, issues, limit, label) {
  const parts = sections(doc)
  for (let i = 0; i < parts.length; i++) {
    const count = sectionWords(doc, parts[i], parts[i + 1])
    if (count > limit) issue(issues, 'SIZE002', doc.path,
      parts[i].heading.position.start.line,
      `${label} '${parts[i].name}' has ${count} words; hard limit ${limit}`)
  }
}

function firstFields(doc) {
  const firstH2 = doc.tree.children.findIndex(n => n.type === 'heading' && n.depth === 2)
  const prefix = firstH2 < 0 ? doc.tree.children : doc.tree.children.slice(0, firstH2)
  const lines = doc.source.split(/\r?\n/u)
  const fields = new Map()
  for (const node of prefix) {
    if (node.type !== 'paragraph') continue
    for (let n = node.position.start.line; n <= node.position.end.line; n++) {
      const match = /^(Status|Feature ID):\s*(.*?)\s*$/u.exec(lines[n - 1])
      if (match) {
        if (!fields.has(match[1])) fields.set(match[1], [])
        fields.get(match[1]).push({value: match[2], line: n})
      }
    }
  }
  return fields
}

function completeness(issues, status, code, path, line, message) {
  issue(issues, code, path, line, message, status !== 'Ready')
}

function hasContent(nodes) {
  return nodes.some(node => {
    if (node.type === 'heading') return false
    return nodeText(node).trim().length > 0
  })
}

function markers(doc, nodes, name) {
  const lines = doc.source.split(/\r?\n/u)
  const found = []
  for (const node of nodes) {
    if (node.type !== 'paragraph') continue
    for (let line = node.position.start.line; line <= node.position.end.line; line++) {
      if (lines[line - 1].trimStart().startsWith(`${name}:`)) found.push({node, line})
    }
  }
  return found
}

function validateStory(doc, section, issues, status) {
  const stories = []
  let story
  for (const node of section.nodes) {
    if (node.type === 'heading' && node.depth === 3) {
      story = {node, name: nodeText(node), nodes: []}
      stories.push(story)
    } else if (story) {
      story.nodes.push(node)
    } else if (node.type !== 'html' && nodeText(node).trim()) {
      issue(issues, 'FB011', doc.path, node.position.start.line,
        'Content in Stories and acceptance must belong to a story')
    }
  }
  const seen = new Set()
  const numbers = []
  for (const item of stories) {
    const line = item.node.position.start.line
    const match = storyPattern.exec(item.name)
    if (!match) {
      issue(issues, 'FB011', doc.path, line, `Invalid story heading '${item.name}'`)
      continue
    }
    const id = `S${match[1]}`
    numbers.push(Number(match[1]))
    if (seen.has(id)) issue(issues, 'FB006', doc.path, line, `Duplicate story ID ${id}`)
    seen.add(id)
    const statements = markers(doc, item.nodes, 'Story')
    const acceptances = markers(doc, item.nodes, 'Acceptance')
    if (statements.length > 1) issue(issues, 'FB008', doc.path,
      statements[1].line, `Story ${id} has more than one Story: statement`)
    if (!statements.length || !nodeText(statements[0].node).replace(/^Story:\s*/u, '').trim()) {
      completeness(issues, status, 'FB008', doc.path, line, `Story ${id} has no Story: statement`)
    }
    if (acceptances.length > 1) issue(issues, 'FB009', doc.path,
      acceptances[1].line, `Story ${id} has more than one Acceptance: block`)
    if (!acceptances.length) {
      completeness(issues, status, 'FB009', doc.path, line, `Story ${id} has no Acceptance: block`)
    } else {
      const index = item.nodes.indexOf(acceptances[0].node)
      const next = item.nodes[index + 1]
      const count = next?.type === 'list'
        ? next.children.filter(n => hasContent(n.children || [])).length : 0
      if (!count) completeness(issues, status, 'FB010', doc.path,
        acceptances[0].line, `Story ${id} has no acceptance criteria`)
    }
  }
  if (numbers.some((number, index) => number !== index + 1)) {
    completeness(issues, status, 'FB007', doc.path,
      stories[0]?.node.position.start.line || section.heading.position.start.line,
      'Story IDs must be sequential from S1')
  }
  return stories.length
}

function validateBrief(doc, issues) {
  const parts = doc.path.split('/')
  if (parts.length !== 4 || parts[0] !== '.workflow' || parts[1] !== 'features' ||
      parts[3] !== 'brief.md' || !featurePattern.test(parts[2])) {
    issue(issues, 'FB017', doc.path, 1, 'Feature Brief must be at .workflow/features/B-xxxx/brief.md')
  }
  const h1 = doc.tree.children.filter(n => n.type === 'heading' && n.depth === 1)
  if (h1.length !== 1 || !nodeText(h1[0]).trim()) {
    issue(issues, 'FB001', doc.path, h1[1]?.position.start.line || 1,
      'Feature Brief must have exactly one nonempty H1')
  } else if (doc.tree.children.find(n => n.type === 'heading') !== h1[0]) {
    issue(issues, 'FB001', doc.path, h1[0].position.start.line,
      'The first heading in a Feature Brief must be its H1')
  }
  const fields = firstFields(doc)
  const statuses = fields.get('Status') || []
  const ids = fields.get('Feature ID') || []
  if (statuses.length !== 1 || !['Draft', 'Ready'].includes(statuses[0].value)) {
    issue(issues, 'FB002', doc.path, statuses[1]?.line || statuses[0]?.line || 1,
      'Status must occur once and be Draft or Ready')
  }
  const status = statuses[0]?.value === 'Ready' ? 'Ready' : 'Draft'
  if (ids.length !== 1 || !featurePattern.test(ids[0].value)) {
    issue(issues, 'FB003', doc.path, ids[1]?.line || ids[0]?.line || 1,
      'Feature ID must occur once and have form B-xxxx')
  } else if (parts[2] !== ids[0].value) {
    issue(issues, 'FB003', doc.path, ids[0].line,
      `Feature ID ${ids[0].value} does not match directory ${parts[2]}`)
  }
  const found = sections(doc)
  const byName = new Map()
  for (const part of found) {
    if (!namedSections.has(part.name)) continue
    if (byName.has(part.name)) issue(issues, 'FB004', doc.path,
      part.heading.position.start.line, `Duplicate section '${part.name}'`)
    else byName.set(part.name, part)
  }
  for (const name of required) {
    const part = byName.get(name)
    if (!part) {
      completeness(issues, status, 'FB004', doc.path, 1, `Missing section '${name}'`)
    } else if (name !== 'Stories and acceptance' &&
        !hasContent(part.nodes.filter(n => n.type !== 'heading'))) {
      completeness(issues, status, 'FB005', doc.path,
        part.heading.position.start.line, `Section '${name}' is empty`)
    }
  }
  for (const name of namedSections) {
    if (required.includes(name)) continue
    const part = byName.get(name)
    if (part && !hasContent(part.nodes.filter(n => n.type !== 'heading'))) {
      completeness(issues, status, 'FB005', doc.path,
        part.heading.position.start.line, `Section '${name}' is empty`)
    }
  }
  for (const part of found) {
    for (const node of part.nodes) {
      if (node.type === 'heading' && node.depth > 2 &&
          part.name !== 'Stories and acceptance') {
        issue(issues, 'FB011', doc.path, node.position.start.line,
          'Subheadings are only valid in Stories and acceptance')
      }
      if (node.type === 'heading' && node.depth > 3) {
        issue(issues, 'FB011', doc.path, node.position.start.line,
          'Story headings must be H3')
      }
    }
  }
  if (byName.has('Stories and acceptance')) {
    const count = validateStory(doc, byName.get('Stories and acceptance'), issues, status)
    if (!count) completeness(issues, status, 'FB005', doc.path,
      byName.get('Stories and acceptance').heading.position.start.line,
      'Stories and acceptance has no stories')
  }
  validateSize(doc, issues, limits.feature_brief, 'Feature Brief')
  return {id: ids[0]?.value, idLine: ids[0]?.line || 1}
}

function linksIn(node) {
  const urls = []
  function visit(current) {
    if (current.type === 'link') urls.push(current.url)
    for (const child of current.children || []) visit(child)
  }
  visit(node)
  return urls
}

function localTarget(source, url) {
  try { return resolve(dirname(source), decodeURIComponent(url.split(/[?#]/u)[0])) }
  catch { return null }
}

function validateBacklog(backlog, briefs, issues) {
  const items = new Map()
  const linkedIds = new Set()
  const invalidLinkedIds = new Set()
  if (backlog) {
    validateSize(backlog, issues, limits.backlog, 'Backlog')
    validateRecords(backlog, issues, limits.backlog_item, 'Backlog item')
    for (const part of sections(backlog)) {
      const match = /^(B-\d{4}):\s+\S/u.exec(part.name)
      if (!match) continue
      const id = match[1]
      if (items.has(id)) issue(issues, 'FB014', backlog.path,
        part.heading.position.start.line, `Duplicate backlog ID ${id}`)
      else items.set(id, part)
    }
    for (const [id, item] of items) {
      const linked = []
      for (const node of item.nodes) {
        if (node.type !== 'list') continue
        for (const child of node.children) {
          const value = nodeText(child).trim()
          if (!/^(Feature Brief|Source):/u.test(value)) continue
          const urls = linksIn(child)
          const briefUrls = urls.filter(url => /(?:^|\/)brief\.md(?:#.*)?$/u.test(url))
          if (value.startsWith('Feature Brief:') || briefUrls.length) {
            linked.push({line: child.position.start.line, urls: briefUrls})
          }
        }
      }
      if (!linked.length) continue
      const canonical = `features/${id}/brief.md`
      const target = resolve(dirname(backlog.file), canonical)
      if (linked.length !== 1 || linked[0].urls.length !== 1 ||
          localTarget(backlog.file, linked[0].urls[0]) !== target) {
        invalidLinkedIds.add(id)
        issue(issues, 'FB013', backlog.path, linked[0].line,
          `Backlog item ${id} must link to ${canonical}`)
      } else linkedIds.add(id)
    }
  }
  const seenIds = new Map()
  for (const {doc, id, idLine} of briefs) {
    if (id && seenIds.has(id)) issue(issues, 'FB016', doc.path, idLine,
      `Feature ID ${id} also occurs in ${seenIds.get(id)}`)
    else if (id) seenIds.set(id, doc.path)
    const directoryId = doc.path.split('/')[2]
    const item = items.get(directoryId)
    if (!item) {
      issue(issues, 'FB012', doc.path, 1, `No backlog item for ${directoryId}`)
      continue
    }
    if (!linkedIds.has(directoryId) && !invalidLinkedIds.has(directoryId)) {
      issue(issues, 'FB013', backlog.path,
        item.heading.position.start.line, `Backlog item ${directoryId} has no Feature Brief link`)
    }
  }
}

function validateOtherSizes(docs, issues) {
  for (const doc of docs) {
    const path = doc.path
    if (path === '.workflow/backlog.md' || path.endsWith('/brief.md')) continue
    if (path === '.workflow/direction.md') validateSize(doc, issues, limits.direction, 'Direction')
    else if (/^\.workflow\/direction\/[^/]+\.md$/u.test(path)) {
      validateSize(doc, issues, limits.direction_topic, 'Direction topic')
    } else if (path === '.workflow/context.md') {
      validateSize(doc, issues, limits.context, 'Context')
      validateRecords(doc, issues, limits.context_entry, 'Context entry')
    } else if (/^\.workflow\/decisions\/pdr\/[^/]+\.md$/u.test(path)) {
      validateSize(doc, issues, limits.pdr, 'PDR')
    } else if (/^\.workflow\/decisions\/adr\/[^/]+\.md$/u.test(path)) {
      validateSize(doc, issues, limits.adr, 'ADR')
    } else if (/^\.workflow\/features\/[^/]+\/acceptance-[^/]+\.md$/u.test(path)) {
      validateSize(doc, issues, limits.acceptance_report, 'Acceptance Report')
    }
  }
}

async function validateMarkdownLinks(root, issues) {
  const files = walk(root, path => /\.md$/iu.test(path)).map(path => pathName(root, path))
  if (!files.length) return
  const context = await new Promise((accept, reject) => engine({
    cwd: root, files, processor: remark, plugins: config.plugins,
    detectConfig: false, detectIgnore: false, reporter: () => ''
  }, (error, _code, result) => error ? reject(error) : accept(result)))
  for (const file of context.files) {
    const path = pathName(root, resolve(root, file.path))
    if (!path.startsWith('.workflow/')) continue
    for (const message of file.messages) {
      const source = message.source || ''
      const isLink = source.startsWith('remark-validate-links:')
      const code = isLink
        ? message.ruleId === 'missing-file' ? 'LINK001' : 'LINK002'
        : 'MD001'
      issue(issues, code, path, message.line || 1, message.reason)
    }
  }
}

export async function check(root) {
  const issues = []
  const workflow = join(root, '.workflow')
  const docs = walk(workflow, path => path.endsWith('.md')).map(path => document(root, path))
  const backlog = docs.find(doc => doc.path === '.workflow/backlog.md')
  const briefs = []
  for (const doc of docs) {
    if (doc.path.endsWith('/brief.md')) briefs.push({doc, ...validateBrief(doc, issues)})
  }
  validateBacklog(backlog, briefs, issues)
  validateOtherSizes(docs, issues)
  await validateMarkdownLinks(root, issues)
  return issues.sort((a, b) => compare(a.path, b.path) ||
    a.line - b.line || compare(a.code, b.code) || compare(a.message, b.message))
}

async function main() {
  const root = resolve(process.argv[2] || '.')
  if (!existsSync(root) || !statSync(root).isDirectory()) {
    console.error(`Not a directory: ${root}`)
    return 2
  }
  if (!existsSync(join(skill, 'node_modules'))) {
    console.error('Run npm ci in the workflow-document-check skill directory.')
    return 2
  }
  try {
    const issues = await check(root)
    for (const finding of issues) {
      console.log(`${finding.code}${finding.warning ? ' warning' : ''} ${finding.path}:${finding.line}\n${finding.message}`)
    }
    if (!issues.length) console.log('Workflow documents passed validation.')
    return issues.some(finding => !finding.warning) ? 1 : 0
  } catch (error) {
    console.error(error.message)
    return 2
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  process.exitCode = await main()
}
