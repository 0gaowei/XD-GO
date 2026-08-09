# Search keyword normalization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Normalize product-search keywords so leading/trailing whitespace is removed and whitespace-only submissions are rejected before they alter search state or make requests.

**Architecture:** Put the pure normalization rule in a small frontend utility and cover it with Node's built-in test runner. The existing Vue search page imports the helper, displays an Element Plus warning for an empty normalized value, and otherwise preserves its present search, suggestion, history, and URL-query flow.

**Tech Stack:** Vue 3 Composition API, Element Plus, Vite, Node.js built-in `node:test`.

---

### Task 1: Add the tested keyword-normalization utility

**Files:**
- Create: `frontend/src/utils/search-keyword.js`
- Create: `frontend/src/utils/search-keyword.test.js`

- [ ] **Step 1: Write the failing utility tests.**

  Add this Node test file:

  ```js
  import test from 'node:test'
  import assert from 'node:assert/strict'
  import { normalizeSearchKeyword } from './search-keyword.js'

  test('removes leading and trailing whitespace', () => {
    assert.equal(normalizeSearchKeyword('  手机  '), '手机')
  })

  test('returns an empty string for whitespace-only input', () => {
    assert.equal(normalizeSearchKeyword(' \n\t '), '')
  })

  test('handles nullish input without throwing', () => {
    assert.equal(normalizeSearchKeyword(null), '')
    assert.equal(normalizeSearchKeyword(undefined), '')
  })
  ```

- [ ] **Step 2: Run the test and verify RED.**

  Run: `node --test frontend/src/utils/search-keyword.test.js`

  Expected: failure because `search-keyword.js` does not yet exist.

- [ ] **Step 3: Add the minimal pure implementation.**

  Create `frontend/src/utils/search-keyword.js`:

  ```js
  export function normalizeSearchKeyword(value) {
    return String(value ?? '').trim()
  }
  ```

- [ ] **Step 4: Verify GREEN.**

  Run: `node --test frontend/src/utils/search-keyword.test.js`

  Expected: three passing tests.

### Task 2: Use normalized keywords in the product-search page

**Files:**
- Modify: `frontend/src/views/shop/search/index.vue`
- Test: `frontend/src/utils/search-keyword.test.js`

- [ ] **Step 1: Add an integration expectation before implementation.**

  In the existing component, identify the current `handleSearch` early return:

  ```js
  const handleSearch = () => {
      if (!keyword.value) return
  ```

  Add the helper import and temporarily use a test-only assertion in `search-keyword.test.js` that the function result for `'  手机  '` is exactly the value that must be stored in `keyword.value` before calling `addToHistory`. This test passes only after the utility exists and locks the component contract to the normalized value.

- [ ] **Step 2: Replace raw keyword use with the normalized flow.**

  Add the import:

  ```js
  import { normalizeSearchKeyword } from '@/utils/search-keyword'
  ```

  Replace `handleSearch` with:

  ```js
  const handleSearch = () => {
      const normalizedKeyword = normalizeSearchKeyword(keyword.value)
      if (!normalizedKeyword) {
          ElMessage.warning('请输入搜索关键词')
          return
      }

      keyword.value = normalizedKeyword
      showSuggestions.value = false
      addToHistory(normalizedKeyword)
      updateQuery()
  }
  ```

  Add `ElMessage` to the existing Element Plus import. In the debounced `handleInput`, compute `const normalizedKeyword = normalizeSearchKeyword(keyword.value)` and use it for the empty check and `getSearchSuggestions(normalizedKeyword)` call.

- [ ] **Step 3: Preserve history and click behavior.**

  In `handleSuggestionClick`, set `keyword.value = normalizeSearchKeyword(item.text)` and call `handleSearch()` rather than duplicating raw history and query writes. Apply the same pattern to `handleHistoryClick` and `handleHotSearchClick` so all entry points use the warning and canonical keyword behavior.

- [ ] **Step 4: Verify the utility and frontend build.**

  Run:

  ```bash
  node --test frontend/src/utils/search-keyword.test.js
  npm --prefix frontend run build
  npx --prefix frontend eslint src/views/shop/search/index.vue src/utils/search-keyword.js
  ```

  Expected: the Node tests and Vite build exit 0. If the repository's current ESLint configuration reports an existing unrelated rule failure, record its exact output and do not reformat unrelated files.

### Task 3: Prepare the narrow LORE smoke-test pull request

**Files:**
- Create: `docs/search-keyword-normalization-design.md`
- Create: `docs/superpowers/plans/2026-08-09-search-keyword-normalization.md`
- Create: `frontend/src/utils/search-keyword.js`
- Create: `frontend/src/utils/search-keyword.test.js`
- Modify: `frontend/src/views/shop/search/index.vue`

- [ ] **Step 1: Inspect the change scope.**

  Run:

  ```bash
  git diff --check
  git status --short
  git diff -- frontend/src/views/shop/search/index.vue frontend/src/utils/search-keyword.js frontend/src/utils/search-keyword.test.js
  ```

  Expected: only the documented design/plan and search keyword files are changed; no backend, database, payment, order, or LORE workflow files are modified.

- [ ] **Step 2: Commit the test PR change.**

  Run:

  ```bash
  git add docs/search-keyword-normalization-design.md docs/superpowers/plans/2026-08-09-search-keyword-normalization.md frontend/src/views/shop/search/index.vue frontend/src/utils/search-keyword.js frontend/src/utils/search-keyword.test.js
  git commit -m "fix: normalize product search keywords"
  ```

- [ ] **Step 3: Push a dedicated PR branch.**

  Run:

  ```bash
  git push --set-upstream origin codex/test-lore-search-keyword
  ```

  Expected: the branch is available to compare against `master`; opening the PR triggers `DeepSeek LORE review` because the LORE workflows already exist on `master`.
