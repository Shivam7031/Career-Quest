<!-- ========================== HEADER =============================== -->

<div align="center" style="font-family: 'Segoe UI', sans-serif;">

  <h1 style="font-size: 48px; font-weight: 900;">🎯 Career Quest</h1>

  <p style="max-width: 780px; font-size: 18px; color: #555;">
    <strong>Career Quest</strong> is an interactive career-guidance platform designed to help users explore
    job roles, assess skills, and find the perfect career pathway. This README includes real-time styled
    components, interactive UI sections, and animated visuals powered directly through HTML & CSS.
  </p>

  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Built_with-HTML_&_CSS-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Version-2.0-orange?style=for-the-badge"/>

</div>

<hr style="border: 1px solid #ccc; margin: 40px 0;">



<!-- =============================================================== -->
<!-- ============= LIVE COMPONENT 1: FLIP CAREER CARDS ============= -->
<!-- =============================================================== -->

<h2>🧩 Live Component 1: Flip Career Cards</h2>

<div style="display:flex; gap:20px; flex-wrap:wrap;">

  <div style="width:260px; height:160px; perspective:800px;">
    <div style="width:100%; height:100%; transition:0.6s; transform-style:preserve-3d;"
         onmouseover="this.style.transform='rotateY(180deg)'"
         onmouseout="this.style.transform='rotateY(0deg)'">

      <div style="position:absolute; width:100%; height:100%; backface-visibility:hidden; background:#4CAF50; color:white; padding:20px; border-radius:12px;">
        <h3>💻 Software Engineer</h3>
        <p>Build and innovate</p>
      </div>

      <div style="position:absolute; width:100%; height:100%; backface-visibility:hidden; background:#2E7D32; color:white; padding:20px; border-radius:12px; transform:rotateY(180deg);">
        <p>Skills: Algorithms, Data Structures, System Design</p>
      </div>

    </div>
  </div>

  <div style="width:260px; height:160px; perspective:800px;">
    <div style="width:100%; height:100%; transition:0.6s; transform-style:preserve-3d;"
         onmouseover="this.style.transform='rotateY(180deg)'"
         onmouseout="this.style.transform='rotateY(0deg)'">

      <div style="position:absolute; width:100%; height:100%; backface-visibility:hidden; background:#2196F3; color:white; padding:20px; border-radius:12px;">
        <h3>📊 Data Analyst</h3>
        <p>Insights & Trends</p>
      </div>

      <div style="position:absolute; width:100%; height:100%; backface-visibility:hidden; background:#0D47A1; color:white; padding:20px; border-radius:12px; transform:rotateY(180deg);">
        <p>Skills: Excel, SQL, Visualization</p>
      </div>

    </div>
  </div>

</div>

<br><br>



<!-- =============================================================== -->
<!-- ================ LIVE COMPONENT 2: TABS SECTION =============== -->
<!-- =============================================================== -->

<h2>📁 Live Component 2: Interactive Tabs (HTML only)</h2>

<div style="border:1px solid #ddd; padding:20px; border-radius:10px; max-width:700px;">

  <style>
    .tab-btn { padding:10px 18px; cursor:pointer; border-radius:6px; display:inline-block; margin-right:10px; background:#eee; }
    .tab-btn:hover { background:#ddd; }
    .tab-box { display:none; padding:15px; }
  </style>

  <div>
    <span class="tab-btn" onclick="this.parentElement.nextElementSibling.children[0].style.display='block'; this.parentElement.nextElementSibling.children[1].style.display='none'; this.parentElement.nextElementSibling.children[2].style.display='none';">Overview</span>
    <span class="tab-btn" onclick="this.parentElement.nextElementSibling.children[0].style.display='none'; this.parentElement.nextElementSibling.children[1].style.display='block'; this.parentElement.nextElementSibling.children[2].style.display='none';">Skills</span>
    <span class="tab-btn" onclick="this.parentElement.nextElementSibling.children[0].style.display='none'; this.parentElement.nextElementSibling.children[1].style.display='none'; this.parentElement.nextElementSibling.children[2].style.display='block';">Careers</span>
  </div>

  <div>
    <div class="tab-box" style="display:block;">Career Quest helps individuals explore skillsets and professional paths.</div>
    <div class="tab-box">Skills assessed: Logical Thinking, Communication, Leadership.</div>
    <div class="tab-box">Careers: Software Engineer, Data Analyst, Designer, Researcher.</div>
  </div>

</div>

<br><br>



<!-- =============================================================== -->
<!-- ================ LIVE COMPONENT 3: FAQ COLLAPSE =============== -->
<!-- =============================================================== -->

<h2>❓ Live Component 3: Expand/Collapse FAQ</h2>

<div style="max-width:750px;">

  <details style="margin-bottom:10px; padding:12px; border:1px solid #ccc; border-radius:8px;">
    <summary style="font-size:17px; font-weight:600;">What is Career Quest?</summary>
    <p style="margin-top:10px;">A platform to explore career paths and skill development.</p>
  </details>

  <details style="margin-bottom:10px; padding:12px; border:1px solid #ccc; border-radius:8px;">
    <summary style="font-size:17px; font-weight:600;">Is it beginner friendly?</summary>
    <p style="margin-top:10px;">Yes, anyone can use it whether a student or professional.</p>
  </details>

  <details style="margin-bottom:10px; padding:12px; border:1px solid #ccc; border-radius:8px;">
    <summary style="font-size:17px; font-weight:600;">Does it provide recommendations?</summary>
    <p style="margin-top:10px;">Yes, based on your assessed skills and preferences.</p>
  </details>

</div>

<br><br>



<!-- =============================================================== -->
<!-- ================ LIVE COMPONENT 4: CSS TOGGLE ================= -->
<!-- =============================================================== -->

<h2>🔘 Live Component 4: CSS Toggle Switch</h2>

<label style="position:relative; display:inline-block; width:60px; height:28px;">
  <input type="checkbox" style="opacity:0; width:0; height:0;" 
         onclick="this.nextElementSibling.style.background=this.checked ? '#4CAF50' : '#ccc'; this.nextElementSibling.children[0].style.transform=this.checked ? 'translateX(32px)' : 'translateX(0px)'">
  <span style="position:absolute; cursor:pointer; top:0; left:0; right:0; bottom:0; background:#ccc; border-radius:34px; transition:0.3s;">
    <span style="position:absolute; height:22px; width:22px; left:4px; bottom:3px; background:white; border-radius:50%; transition:0.3s;"></span>
  </span>
</label>

<br><br>



<!-- =============================================================== -->
<!-- ================ LIVE COMPONENT 5: SEARCH BAR ================= -->
<!-- =============================================================== -->

<h2>🔍 Live Component 5: Styled Search Bar</h2>

<div style="max-width:500px;">
  <input type="text" placeholder="Search for careers..." 
         style="width:100%; padding:12px; border-radius:8px; border:1px solid #aaa; font-size:16px;">
</div>

<br><br>



<!-- =============================================================== -->
<!-- ============== LIVE COMPONENT 6: PROGRESS RINGS =============== -->
<!-- =============================================================== -->

<h2>⭕ Live Component 6: Circular Skill Rings</h2>

<div style="display:flex; gap:40px; flex-wrap:wrap;">

  <div style="text-align:center;">
    <svg width="120" height="120">
      <circle cx="60" cy="60" r="50" stroke="#eee" stroke-width="10" fill="none"></circle>
      <circle cx="60" cy="60" r="50" stroke="#4CAF50" stroke-width="10" fill="none"
              stroke-dasharray="314" stroke-dashoffset="60" transform="rotate(-90 60 60)"></circle>
    </svg>
    <p>Logical Thinking – 80%</p>
  </div>

  <div style="text-align:center;">
    <svg width="120" height="120">
      <circle cx="60" cy="60" r="50" stroke="#eee" stroke-width="10" fill="none"></circle>
      <circle cx="60" cy="60" r="50" stroke="#2196F3" stroke-width="10" fill="none"
              stroke-dasharray="314" stroke-dashoffset="100" transform="rotate(-90 60 60)"></circle>
    </svg>
    <p>Communication – 70%</p>
  </div>

</div>

<br><br>



<!-- =============================================================== -->
<!-- ==================== REST OF README =========================== -->
<!-- =============================================================== -->

<hr>

<h2>📂 Folder Structure</h2>

<pre style="background:#f4f4f4; padding:18px; border-radius:8px;">
Career-Quest/
│── index.html
│── style.css
│── /assets
│     ├── images/
│     └── icons/
</pre>

<hr>

<h2>⚙️ Setup</h2>

<pre style="background:#f4f4f4; padding:18px; border-radius:8px;">
git clone https://github.com/your-username/career-quest.git
cd career-quest
open index.html
</pre>

<hr>

<h2>📬 Contact</h2>

<p>Email: your-email@example.com<br>
GitHub: <a href="https://github.com/your-username">your-username</a></p>

<br><br>
