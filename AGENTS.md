
<!-- BEGIN VILLA-KB INSTRUCTION -->
# Villa knowledge base — read it first, write back to it always

Vault: `~/stacks/villa-knowledge-base` · Published: https://knowledge.villamarket.ai

**Read it before you debug.**

```bash
KB=~/stacks/villa-knowledge-base
if [ -d "$KB" ]; then
  git -C "$KB" pull --rebase --quiet
elif git clone -q git@github.com:villa-market/villa-knowledge-base.git "$KB" 2>/dev/null; then
  :                                    # an SSH key is present — a workstation
elif [ -n "${KB_TOKEN:-}" ] && git -c credential.helper='!f(){ echo username=x-access-token; echo "password=$KB_TOKEN"; };f' \
       clone -q https://github.com/villa-market/villa-knowledge-base.git "$KB" 2>/dev/null; then
  :                                    # only if an environment happens to set one;
                                       # no KB_TOKEN is issued today — do not ask for it
else
  unset KB                             # no clone — use Tailscale /auth/agent, not an unauthenticated fetch
fi
rg -i "<the reporter's exact words>" "$KB/content" -l
rg -l "systems:.*<service>" "$KB/content"
```

## The Mac is the source — read and write through it

**The workstation clone at `~/stacks/villa-knowledge-base` is the canonical
working copy, and its SSH key is the only credential involved.** No token, no
secret, nothing to renew. If you are running on the Mac — Claude Code, Cursor,
Kimi, Codex, Gemini, Grok — you already have full read **and write** access. Use it:

```bash
KB=~/stacks/villa-knowledge-base
git -C "$KB" pull --rebase --quiet          # first, always
rg -i "<the reporter's exact words>" "$KB/content" -l
# …write the note…
git -C "$KB" add content/incidents/<your-note>.md
git -C "$KB" commit -m "why it broke, not just what you touched"
git -C "$KB" push                            # pushing to main publishes in ~2 min
```

That is the whole write-back path. Do not look for a token and do not ask for
one — on this machine there is nothing to configure.

**If you are not on the Mac**, you have no credential and are not going to get
one. `/home/ubuntu` or any home that is not `/Users/nic` means a sandbox with
its own filesystem and its own git config. Fetch the site with a session (below),
and hand the write-back back to the Mac: end your run by printing the note **as
a complete file** — full frontmatter, final wording, and the exact path it
belongs at — so a Mac-side agent or person can commit it verbatim instead of
reconstructing it from a summary.

```
PATH: content/incidents/2026-08-09-<slug>.md
---
title: …
type: incident
…
---
<the whole note>
```

A summary that says "I learned X, someone should write it up" loses the detail
that made it worth recording. The point of writing it out in full is that the
Mac side becomes a paste, not a rewrite.

> **If the clone fails, read the site with a session instead.**
>
> The repo is private, so `Repository not found` or `Permission denied (publickey)`
> means **you are not a collaborator**, not that the URL is wrong. Do not retry it,
> do not hunt for a typo, and do not report the vault as missing. Some machines
> also rewrite `git@github.com:` to HTTPS, which is why the error can name a URL
> you never typed.
>
> **Nothing on the site is public.** Every note and both search indexes return
> `401` without a session. Only `/login`, `/auth*` and CSS/JS/images answer to
> anyone. There are two ways to get a session:
>
> - **On the villa tailnet:** one HTTP GET to the Tailscale login server on
>   `doconnect-sf`, no browser (below). Since 2026-09-25 it is the only login
>   server holding the current session key. Tokens from `composer-try` or
>   `doconnect:8443` are rejected with `401` until they are updated.
> - **Off the tailnet, with an API key** you were given through the Villa vault
>   (`kbk_…`): send it as `Authorization: Bearer $KB_API_KEY` on any page.
> - **Off the tailnet, without one:** `curl -fsSL https://knowledge.villamarket.ai/auth/agent | bash`
>   tries the Tailscale servers, then signs a challenge with an SSH key that is
>   registered on your GitHub account. That works for the repo's collaborators
>   (copied into the auth stack's allowlist) and for site readers. There is no GitHub sign-in.
>
> **If you have neither, stop and ask nic** for access. Say what you need to read and
> why. Do not look for another way in, and do not guess a note's contents.
>
> With a session, search the indexes with the Bearer token:
>
> ```bash
> TOKEN=$(curl -fsS https://doconnect-sf.taile8dc37.ts.net/token | python3 -c 'import json,sys; print(json.load(sys.stdin)["token"])')
> curl -sS -H "Authorization: Bearer $TOKEN" \
>   https://knowledge.villamarket.ai/static/symptom-index.json -o /tmp/kb-sym.json
> curl -sS -H "Authorization: Bearer $TOKEN" \
>   https://knowledge.villamarket.ai/static/contentIndex.json -o /tmp/kb-txt.json
> python3 - "<the reporter's exact words>" <<'PY'
> import json, re, sys
> words = [w for w in re.findall(r"\w+", sys.argv[1].lower()) if len(w) > 3]
> sym = json.load(open('/tmp/kb-sym.json')); txt = json.load(open('/tmp/kb-txt.json'))
> hits = {}
> for slug, e in sym.items():                    # the reporter's own words first
>     blob = " ".join(e.get('symptoms', [])).lower()
>     if blob and all(w in blob for w in words):
>         hits[slug] = ("symptom", e.get('title', slug))
> for slug, e in txt.items():                    # then full note text
>     if slug not in hits and all(w in (e['title'] + e['content']).lower() for w in words):
>         hits[slug] = ("text", e['title'])
> for slug, (how, title) in sorted(hits.items(), key=lambda kv: kv[1][0]):
>     print(f"[{how:7}] https://knowledge.villamarket.ai/{slug} — {title}")
> PY
> ```
>
> Then read any hit with `curl -sS -H "Authorization: Bearer $TOKEN" <url>`.
> If `TOKEN` is empty or a fetch returns `401`, you have no valid session: use
> `/auth/agent` as above, or ask nic. Don't retry the same request.
>
> `symptom-index.json` exists because Quartz strips frontmatter from its own
> index, so without it the reporter's verbatim `symptoms:` would be unsearchable
> from the site — the one axis you most want.
>
> With a session you can **read** but **write** nothing. To write back,
> ask nic for collaborator access on `villa-market/villa-knowledge-base`. Until
> you have it, put the note you would have written in your summary so a person
> can commit it — do not silently skip the write-up.

Search the reporter's wording first — `symptoms:` frontmatter records verbatim
complaints, because testers describe behaviour rather than causes.

Every coupon failure investigated on dev through July 2026 traced to a *consumer*
of a service, not to the service itself. Confirm the raw API response before
changing a calculator.

## Two traps that have each cost days

Before concluding a dev fix "isn't live", read `content/systems/dev-environment.md`.
A correct file in S3 plus a completed CloudFront invalidation still serves stale
code — the service worker precache revision must change too.

Before changing discount or shipping maths, read `content/reference/discount-fields.md`.
It is the written contract between VillaCoupon3, calculatecost2 and the storefront;
two production bugs came from a consumer disregarding it.

**Writing back is not optional.** You are the primary author here: people review
what you write but are not expected to write notes themselves. Work is not
complete until the knowledge base reflects it — treat it like `git push`. Do not
defer the write-up to a human or ask permission to record something.

| When you | Write |
|---|---|
| fixed a bug | dated note in `content/incidents/`, `symptoms:` in the reporter's own words |
| changed how a service behaves | `content/systems/<service>.md`, plus `content/reference/coupon-types.md` or `discount-fields.md` if the consumer contract moved |
| learned something undocumented | add it even if nothing was broken |
| ran a procedure twice | make it a runbook |
| found a note stale | correct it; append `## Follow-up` to incidents rather than rewriting them |

Record what you **measured**, not just what you concluded — the numbers, the
command you ran, and the wrong turns worth saving the next person. If a claim in
the repo turned out to be wrong, say so explicitly.

```bash
cd "$KB" && git pull --rebase                 # first, always
git add content/incidents/<your-note>.md      # name your files — never `git add -A`
git commit -m "why it broke, not just what you touched" && git push
```

Pushing to `main` publishes in about two minutes. **Do not run `infra/publish.sh`** —
it needs AWS credentials you probably do not have, it builds from your working
tree rather than from `main`, and running it before pulling silently reverts
whatever a colleague pushed in the meantime. It exists for debugging the build.

`git add -A` is how another session's half-finished work, and iCloud `note 2.md`
conflict copies, end up in your commit. Both have happened.

If you genuinely learned nothing worth recording, say so in your summary rather
than skipping silently.

## Taskworld — create and update project tasks

Villa engineering work must also land on the matching Taskworld board (workspace
**villamarket**). Same completion bar as the vault write-back.

| Tooling | |
|---|---|
| Runbook | https://knowledge.villamarket.ai/runbooks/sync-taskworld-tasks |
| System note | https://knowledge.villamarket.ai/systems/taskworld |
| Bridge | `~/stacks/taskworld-task-management` |

**Credentials** (never commit; never paste into chat):

```bash
# Secret: taskworld-api · region ap-southeast-1 · AWS_PROFILE=villaai or default
aws secretsmanager get-secret-value \
  --secret-id taskworld-api --region ap-southeast-1 \
  --query SecretString --output text
# → write KEY=value to ~/.taskworld (mode 600), or export TASKWORLD_* /
#   TASKWORLD_LOAD_AWS_SECRET=1 for the bridge CLI
```

After a feature or fix: create or complete a task on that system’s board
(**Features** / **Fixes** / **Platform** / **Docs** / **To Do**). Put hours in
the title as `(Nh)`. Board IDs are in the bridge `config/project-map.yaml`.
<!-- END VILLA-KB INSTRUCTION -->
