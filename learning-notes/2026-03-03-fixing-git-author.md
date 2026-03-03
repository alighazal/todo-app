## Fixing Git Author & Email on Existing Commits

- **Context**
  - I initially committed to this repo with the wrong `user.name` / `user.email`.
  - I fixed my global/local config using:
    - `git config --global user.name "Correct Name"`
    - `git config --global user.email "correct@example.com"`
  - I then needed to rewrite existing commits so their author/committer metadata matches the new config.

- **One-shot rewrite of all commits from the first one (fresh repo, not yet pushed)**
  - From the repo root:
    - `git rebase --root --exec 'git commit --amend --reset-author -CHEAD'`
  - What this does:
    - Replays every commit starting from the very first one.
    - For each commit, runs `git commit --amend --reset-author -CHEAD`:
      - `--reset-author` updates the author + committer to match current git config.
      - `-CHEAD` keeps the same commit message.
  - After it completes:
    - Verify authors:
      - `git log --format="%h %an <%ae>"`
    - First push (no force needed because the branch has never been pushed before):
      - `git push -u origin main`  # or the actual branch name

- **Alternative: interactive rebase from root (manual but explicit)**
  - `git rebase -i --root`
  - In the editor, change every `pick` to `edit` (or `e`), then save/quit.
  - For each commit stop:
    - `git commit --amend --reset-author`
    - `git rebase --continue`
  - After the last commit is rewritten, again verify with:
    - `git log --format="%h %an <%ae>"`

- **When a force push is needed vs not**
  - **Not needed**:
    - Fresh repo, branch has never been pushed:
      - After rewriting, just do `git push -u origin main`.
  - **Needed**:
    - If the wrong-author commits were already pushed:
      - After the rebase, use:
        - `git push --force-with-lease`
      - This rewrites remote history, so collaborators must resync.

