╔════════════════════════════════════════════════════════════════════════════╗
║              GITHUB SETUP - STEP BY STEP                                 ║
╚════════════════════════════════════════════════════════════════════════════╝

STEP 1: CREATE GITHUB REPOSITORY
════════════════════════════════════════════════════════════════════════════

1. Go to github.com and login
2. Click "+" (top right) → "New repository"
3. Name: quantlens
4. Description: "ML Market Regime & Risk Analyzer"
5. Public (so people can see it)
6. Click "Create repository"

You'll see a page with commands. Copy the repo URL (looks like):
  https://github.com/yourusername/quantlens.git

════════════════════════════════════════════════════════════════════════════

STEP 2: INITIALIZE GIT LOCALLY
════════════════════════════════════════════════════════════════════════════

Open terminal in your project folder:

cd "D:\project ideas\stock condition"

Then initialize git:

git init

Add all files:

git add .

Commit:

git commit -m "Initial commit: QuantLens ML market regime analyzer"

════════════════════════════════════════════════════════════════════════════

STEP 3: CONNECT TO GITHUB
════════════════════════════════════════════════════════════════════════════

Set remote (replace yourusername):

git remote add origin https://github.com/yourusername/quantlens.git

Verify:

git remote -v

Should show:
  origin  https://github.com/yourusername/quantlens.git (fetch)
  origin  https://github.com/yourusername/quantlens.git (push)

════════════════════════════════════════════════════════════════════════════

STEP 4: PUSH TO GITHUB
════════════════════════════════════════════════════════════════════════════

Push (this uploads your code):

git branch -M main

git push -u origin main

Enter your GitHub username and password (or personal access token).

Done! Check github.com/yourusername/quantlens — your code is live!

════════════════════════════════════════════════════════════════════════════

STEP 5: ADD GITHUB TOPICS (FOR DISCOVERABILITY)
════════════════════════════════════════════════════════════════════════════

Go to github.com/yourusername/quantlens

Click "Settings" (top right)

Scroll down to "Topics"

Add these tags:
  ✓ machine-learning
  ✓ finance
  ✓ python
  ✓ streamlit
  ✓ data-science
  ✓ k-means
  ✓ time-series
  ✓ unsupervised-learning

Save. Now your project is discoverable!

════════════════════════════════════════════════════════════════════════════

STEP 6: VERIFY FILES ON GITHUB
════════════════════════════════════════════════════════════════════════════

Should see:
  ✓ README.md
  ✓ app.py
  ✓ data.py
  ✓ features.py
  ✓ model.py
  ✓ eda.py
  ✓ requirements.txt
  ✓ LICENSE
  ✓ .gitignore

(NOT visible due to .gitignore):
  ✗ .venv/
  ✗ __pycache__/
  ✗ *.log

Perfect!

════════════════════════════════════════════════════════════════════════════

QUICK COMMAND SUMMARY (Copy-Paste)
════════════════════════════════════════════════════════════════════════════

cd "D:\project ideas\stock condition"
git init
git add .
git commit -m "Initial commit: QuantLens ML market regime analyzer"
git remote add origin https://github.com/yourusername/quantlens.git
git branch -M main
git push -u origin main

════════════════════════════════════════════════════════════════════════════

ISSUES? 
════════════════════════════════════════════════════════════════════════════

"fatal: The current branch main does not have any upstream tracking information"
→ Run: git push -u origin main

"Permission denied (publickey)"
→ You may need to set up SSH keys or use a personal access token
  See: https://docs.github.com/en/github/authenticating-to-github

"Nothing to commit"
→ Make sure you're in the right folder with the .git directory

════════════════════════════════════════════════════════════════════════════

AFTER PUSHING: LINKEDIN POST
════════════════════════════════════════════════════════════════════════════

Post one of the templates from LINKEDIN_POSTS.md
Include link: https://github.com/yourusername/quantlens

Now your project is visible to recruiters, tech leads, and community!

════════════════════════════════════════════════════════════════════════════
