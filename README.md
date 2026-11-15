# Garcha NDA Coach

NDA written-exam prep app: syllabus tracker, verified shortcuts, daily recall, weekly and monthly tests (real marking), and a current-affairs feed that updates itself every day. Works offline and installs on phones.

## Put it on GitHub and get a share link (about 5 minutes)
1. On github.com, create a **public** repository named `garcha-nda-coach` (free Pages needs a public repo).
2. Upload every file and folder from this directory, including the hidden `.github` folder (drag them into the repo page, or use git).
3. Repo **Settings > Pages**: Source = "Deploy from a branch", Branch = `main`, Folder = `/ (root)`. Save.
4. Repo **Settings > Actions > General > Workflow permissions**: choose "Read and write permissions". Save.
5. Repo **Actions** tab > "Update current affairs" > **Run workflow** once (it then runs daily at 07:00 IST).
6. Share this link: `https://<your-github-username>.github.io/garcha-nda-coach/`

## Installing on a phone
- **Android (Chrome):** open the link, tap **Install app** (top right) or the browser menu > Install app.
- **iPhone (Safari):** open the link, tap Share > **Add to Home Screen**.

## How updates work
- `scripts/fetch_feed.py` pulls public news feeds into `data/current_affairs.json` daily. No AI and no server needed.
- `data/questions.json` is the shared extra question bank. Add questions there (format below) and everyone gets them on next open.
- After changing `index.html`, bump `VERSION` in `sw.js` so phones pick up the new version.

Question format: `[{"s":"Physics","u":"Units","q":"...","o":["A","B","C","D"],"a":1,"e":"explanation"}]` where `a` is the index (0-3) of the right option.

## Limits
- Progress is stored on each person's own phone (not shared, not backed up). Use Bank and backup > Export data.
- Current-affairs items are headlines from news feeds. Read the source before relying on a fact.
- Confirm exam dates, vacancies and pattern in the official UPSC notice (upsc.gov.in).
