import test from 'node:test'
import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { normalizeSearchKeyword } from './search-keyword.js'

test('normalizes surrounding whitespace from a keyword', () => {
    assert.equal(normalizeSearchKeyword('  wireless headphones  '), 'wireless headphones')
})

test('normalizes whitespace-only input to an empty keyword', () => {
    assert.equal(normalizeSearchKeyword(' \t\n '), '')
})

test('normalizes nullish input to an empty keyword', () => {
    assert.equal(normalizeSearchKeyword(null), '')
    assert.equal(normalizeSearchKeyword(undefined), '')
})

test('converts non-nullish values to strings before trimming', () => {
    assert.equal(normalizeSearchKeyword(123), '123')
})

test('normalizes the keyword before updateQuery writes the route query', async () => {
    const source = await readFile(new URL('../views/shop/search/index.vue', import.meta.url), 'utf8')

    assert.match(source, /const normalizedKeyword = normalizeSearchKeyword\(keyword\.value\)/)
    assert.match(source, /keyword\.value = normalizedKeyword/)
    assert.match(source, /keyword: normalizedKeyword \|\| undefined/)
})
