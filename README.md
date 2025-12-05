<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Career Quest — README</title>
  <link rel="stylesheet" href="./README.css" />
</head>
<body>
  <header class="hero">
    <div class="container">
      <h1>Career Quest</h1>
      <p class="tagline">Full‑stack career counselling & course recommendation app (React + Vite frontend, Flask backend)</p>
    </div>
  </header>

  <main class="container">
    <section>
      <h2>Overview</h2>
      <p>Career Quest predicts courses based on user interests, recommends Coursera courses using TF‑IDF similarity, and supports interview-question generation with audio evaluation.</p>
    </section>

    <section>
      <h2>Repository layout (high level)</h2>
      <ul>
        <li><strong>/backend</strong> — Flask app, ML pipeline, recommender helpers, templates and CSV datasets.</li>
        <li><strong>/frontend</strong> — React + Vite TypeScript app (UI, chatbot components).</li>
        <li><strong>README.html / README.css</strong> — this file and stylesheet.</li>
      </ul>
    </section>

    <section>
      <h2>Quick start — Backend (Flask)</h2>
      <ol>
        <li>Create a Python virtual env:
          <pre>python -m venv .venv
.venv\Scripts\activate</pre>
        </li>
        <li>Install deps:
          <pre>pip install -r backend/requirements.txt</pre>
        </li>
        <li>Set environment variables (example):
          <pre>set GEMINI_API_KEY=your_key_here</pre>
        </li>
        <li>Run:
          <pre>cd backend
python app.py</pre>
        </li>
      </ol>
    </section>

    <section>
      <h2>Quick start — Frontend (React + Vite)</h2>
      <ol>
        <li>Install Node (>=16), then:
          <pre>cd frontend
npm install
npm run dev</pre>
        </li>
        <li>Open the dev URL shown by Vite (default: http://localhost:5173).</li>
      </ol>
    </section>

    <section>
      <h2>Important files & endpoints</h2>
      <ul>
        <li><code>backend/app.py</code> — Flask routes, ML orchestration, Gemini integration.</li>
        <li><code>backend/course.py</code> — TF‑IDF & recommender helpers.</li>
        <li><code>backend/Courser.csv</code>, <code>backend/stud_training.csv</code> — datasets.</li>
        <li>Frontend entry: <code>frontend/src/main.tsx</code>, UI: <code>frontend/src/App.tsx</code>.</li>
      </ul>
    </section>

    <section>
      <h2>Data & credentials</h2>
      <ul>
        <li>Place Coursera CSV at <code>backend/Courser.csv</code>.</li>
        <li>Set <code>GEMINI_API_KEY</code> in environment for Gemini features.</li>
      </ul>
    </section>

    <section>
      <h2>Troubleshooting</h2>
      <ul>
        <li>If recommender returns no results: broaden keywords — it relies on course "Skills" text.</li>
        <li>For Gemini / API errors: confirm <code>GEMINI_API_KEY</code> and network access.</li>
      </ul>
    </section>

    <section class="footer-note">
      <h3>Contributing & License</h3>
      <p>Fork, create a branch, add tests, and open a PR. Add a LICENSE file before publishing.</p>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">Career Quest — local README view</div>
  </footer>
</body>
</html>
