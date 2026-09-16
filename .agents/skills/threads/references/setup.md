# Threads API: setup, auth & tokens

How the app gets wired up, and how to refresh/rebuild the token. The day-to-day skill
(posting, metrics) doesn't need any of this. It's here for token refresh and disaster
recovery.

## What you end up with

Once wired and working, credentials live in a gitignored creds file and the working token
is in `.env` as `THREADS_ACCESS_TOKEN` / `THREADS_USER_ID`. Fill this table in for your own
app (keep it in a gitignored file, not a committed one):

| Thing              | Value                                                        |
| ------------------ | ------------------------------------------------------------ |
| Meta app ID        | `<META_APP_ID>` (dashboard URLs, app roles)                  |
| Threads app ID     | `<THREADS_APP_ID>` (OAuth `client_id`, the one the API uses) |
| Account / tester   | `<your-handle>` (Threads Tester, invite accepted)            |
| Numeric user id    | `<THREADS_USER_ID>`                                          |
| Account id         | `<ACCOUNT_ID>` (distinct; shows up in insights URLs)         |
| Redirect callback  | `https://<your-site>/api/callback`                           |
| Uninstall / Delete | `https://<your-site>/api/{uninstall,delete}`                 |

> **Don't confuse the two app IDs.** The Threads app ID is the OAuth `client_id` the API uses;
> the Meta app ID is for dashboard URLs and app roles. Keep the Meta app secret and the access
> token in gitignored files only, never committed and never echoed through a shell command
> (which lands in transcripts). If either is ever exposed, regenerate both from the dashboard in
> seconds; the scripts won't care, since they read `.env`.

## The path that actually worked: User Token Generator

This skips the manual OAuth code dance entirely.

1. **Threads use case** added to the Meta app; permissions added until "Ready for testing"
   (see scopes below).
2. **Settings, callback URLs.** The Redirect Callback URLs field is a _tag_ input: type the
   URL and press **Enter / click the suggestion** so it becomes a chip. Just typing + Save
   fails with "Please specify an OAuth redirect URI." All three fields are required to save.
3. **App roles, Threads Testers, Add People, Threads Tester, `<your-handle>`.** Sends an
   invite (account must be **public**).
4. **Accept the invite in Threads:** Settings, Account, Website permissions, **Invites**,
   Accept `<your-site>`.
5. **Settings, User Token Generator, Generate Access Token** for the tester, a 60-day
   long-lived token. Paste into `.env` (in an editor, not a shell command that echoes it).
6. Fetch the numeric user id: `GET /me?fields=id,username&access_token=…`, that is `THREADS_USER_ID`.

## Scopes (all five added)

| Scope                     | Needed for                                 |
| ------------------------- | ------------------------------------------ |
| `threads_basic`           | **everything**, required on every endpoint |
| `threads_content_publish` | creating posts/replies                     |
| `threads_read_replies`    | `GET` replies / conversations              |
| `threads_manage_replies`  | posting/hiding replies                     |
| `threads_manage_insights` | reading post + account metrics             |

Post-only would need just the first two.

## Token lifecycle

60-day long-lived token. **Refresh before day 60** (resets to 60 days):

```bash
GET https://graph.threads.net/refresh_access_token?grant_type=th_refresh_token&access_token=<LONG>
```

A refreshed token is the simplest fix if posting starts 400ing on auth. If the token is fully
dead, re-run the User Token Generator (steps 5 and 6 above); no need to redo the app config.

## Manual OAuth flow (alternative to the token generator)

Only needed if generating tokens for accounts other than the tester, or building a real
login. Three hops:

1. **Authorize** (browser): `https://threads.net/oauth/authorize?client_id=<THREADS_APP_ID>&redirect_uri=<URI>&scope=threads_basic,threads_content_publish,…&response_type=code`
   redirects to `<URI>?code=…` (code valid 1 hour).
2. **Code to short-lived token** (1 hr): `POST https://graph.threads.net/oauth/access_token`
   with `client_id`, `client_secret`, `grant_type=authorization_code`, `redirect_uri`, `code`.
3. **Short to long-lived** (60 days):
   `GET https://graph.threads.net/access_token?grant_type=th_exchange_token&client_secret=<SECRET>&access_token=<SHORT>`

> The exchange/refresh endpoints mirror the Instagram Basic Display pattern; if one errors,
> check the current "Get Access Tokens" doc.

## Security

The token posts **as you** (the account owner) and is effectively a password. Keep it in `.env`
(gitignored), never in committed files, never echoed through a shell command (which lands in
transcripts). Both the token and the Meta app secret are revocable/regenerable from the
dashboard in seconds.

## Official docs

- Get started / tokens: https://developers.facebook.com/docs/threads/get-started
- Posts & publishing: https://developers.facebook.com/docs/threads/posts
- Reply management: https://developers.facebook.com/docs/threads/reply-management
- Insights: https://developers.facebook.com/docs/threads/insights
- Changelog (check for drift): https://developers.facebook.com/docs/threads/changelog
