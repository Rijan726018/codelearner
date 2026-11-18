# CodeBay (codebay.org)

Static vanilla-JS learning site: lessons, bootcamp, problems, career paths, Code Auction. See README.md for the map.

## Shipping a change: always finish with a release

codebay.org is served by the Vercel project of the private repo `Rijan726018/codebay`, which builds the codelearner
commit named in its `codelearner.sha`. Merging here does NOT update codebay.org on its own. After every merge to
`main` in this repo:

1. In `Rijan726018/codebay` (branch off `master`), set `codelearner.sha` to this repo's new `main` commit
   (`git rev-parse origin/main`), commit, push, open a PR ("Release codelearner <short sha>: <what changed>") and merge it.
   Vercel deploys merges to `master` automatically.
2. About a minute later, check codebay.org serves the new files, e.g. compare
   `curl -sSL https://codebay.org/<file> | md5sum` with `git show origin/main:<file> | md5sum` for the files you changed.
3. If `firestore.rules` changed, tell the user to paste it into Firebase → Firestore → Rules → Publish (it is not
   deployed by this flow).

Never ask the user to press Redeploy in Vercel for a normal update; the release PR does it.
