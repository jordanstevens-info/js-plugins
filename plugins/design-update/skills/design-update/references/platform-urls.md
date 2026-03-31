# Platform URL Construction

Rules for deriving web URLs from `git remote get-url origin` output.

---

## Parsing the Remote URL

Git remotes come in two formats. Extract the host, org, and repo from either:

### HTTPS Format

```
https://github.com/org-name/repo-name.git
https://gitlab.com/org-name/repo-name.git
```

Pattern: `https://<host>/<org>/<repo>.git`

Strip the trailing `.git` suffix if present.

### SSH Format

```
git@github.com:org-name/repo-name.git
git@gitlab.com:org-name/repo-name.git
```

Pattern: `git@<host>:<org>/<repo>.git`

Extract `<host>` from after `@` and before `:`. Extract `<org>/<repo>` from after
`:`. Strip the trailing `.git` suffix if present.

---

## GitHub URL Patterns

Host: `github.com`

| Resource | URL Pattern |
|----------|-------------|
| Branch | `https://github.com/<org>/<repo>/tree/<branch-name>` |
| File on branch | `https://github.com/<org>/<repo>/blob/<branch-name>/<file-path>` |
| Compare | `https://github.com/<org>/<repo>/compare/main...<branch-name>` |

---

## GitLab URL Patterns

Host: `gitlab.com` (or self-hosted GitLab instances)

| Resource | URL Pattern |
|----------|-------------|
| Branch | `https://<host>/<org>/<repo>/-/tree/<branch-name>` |
| File on branch | `https://<host>/<org>/<repo>/-/blob/<branch-name>/<file-path>?ref_type=heads` |
| Compare | `https://<host>/<org>/<repo>/-/compare/main...<branch-name>` |

Note the `/-/` path segment that distinguishes GitLab URLs from GitHub URLs.

---

## Platform Detection

Determine the platform from the extracted host:

| Host contains | Platform |
|---------------|----------|
| `github.com` | GitHub |
| `gitlab.com` | GitLab |
| `gitlab` (any subdomain, e.g. `gitlab.company.com`) | GitLab (self-hosted) |

For self-hosted GitLab, use the full host as the base URL instead of `gitlab.com`.

---

## Unknown Host

If the remote host does not match any known pattern, ask the user for the web base
URL before constructing links. Do not guess — an incorrect URL is worse than no URL.
