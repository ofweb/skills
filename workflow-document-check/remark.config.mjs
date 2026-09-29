import remarkGfm from 'remark-gfm'
import remarkLintCorrectMediaSyntax from 'remark-lint-correct-media-syntax'
import remarkLintHeadingIncrement from 'remark-lint-heading-increment'
import remarkLintNoDuplicateDefinitions from 'remark-lint-no-duplicate-definitions'
import remarkLintNoEmptyUrl from 'remark-lint-no-empty-url'
import remarkLintNoHeadingLikeParagraph from 'remark-lint-no-heading-like-paragraph'
import remarkLintNoUndefinedReferences from 'remark-lint-no-undefined-references'
import remarkValidateLinks from 'remark-validate-links'

export default {
  plugins: [
    remarkGfm,
    remarkLintCorrectMediaSyntax,
    remarkLintHeadingIncrement,
    remarkLintNoDuplicateDefinitions,
    remarkLintNoEmptyUrl,
    remarkLintNoHeadingLikeParagraph,
    remarkLintNoUndefinedReferences,
    [remarkValidateLinks, {repository: false}]
  ]
}
