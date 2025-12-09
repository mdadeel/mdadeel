<!-- Animated header: paste this at the very top of your README.md -->
<div align="center">
  <!-- Animated SVG header: neon gradient + type-reveal + blinking cursor -->
  <!-- Width scales on GitHub. If GitHub strips this, save as ./assets/header.svg and embed with an image. -->
  <svg role="img" viewBox="0 0 1200 220" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">
    <defs>
      <!-- animated gradient -->
      <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="0%">
        <stop offset="0%" stop-color="#7f5af0">
          <animate attributeName="stop-color" dur="6s" values="#7f5af0;#0ea5e9;#06b6d4;#7f5af0" repeatCount="indefinite"/>
        </stop>
        <stop offset="50%" stop-color="#06b6d4">
          <animate attributeName="stop-color" dur="6s" values="#06b6d4;#7c3aed;#f43f5e;#06b6d4" repeatCount="indefinite"/>
        </stop>
        <stop offset="100%" stop-color="#f43f5e">
          <animate attributeName="stop-color" dur="6s" values="#f43f5e;#7f5af0;#0ea5e9;#f43f5e" repeatCount="indefinite"/>
        </stop>
      </linearGradient>

      <!-- neon glow filter -->
      <filter id="neon">
        <feGaussianBlur stdDeviation="4" result="b"/>
        <feMerge>
          <feMergeNode in="b"/>
          <feMergeNode in="SourceGraphic"/>
        </feMerge>
      </filter>

      <!-- masking rectangle used for type-reveal -->
      <mask id="revealMask">
        <rect x="0" y="0" width="0" height="220" fill="#fff">
          <!-- expand mask to reveal text -->
          <animate attributeName="width" from="0" to="1200" dur="3.6s" begin="0.4s" fill="freeze" />
        </rect>
      </mask>
    </defs>

    <!-- soft background -->
    <rect width="100%" height="100%" rx="10" fill="black" opacity="0.85"/>

    <!-- big neon title (will be revealed by mask) -->
    <g mask="url(#revealMask)">
      <text x="50" y="110" font-family="ui-monospace, SFMono-Regular, Menlo, Monaco, 'Roboto Mono', monospace"
            font-size="48" letter-spacing="1.2" fill="url(#g)" filter="url(#neon)">
        Adeel <tspan font-weight="600">|</tspan> Creative Developer &amp; Tech Educator
      </text>

      <!-- animated underline sweep -->
      <rect x="50" y="130" width="0" height="6" rx="3" fill="url(#g)">
        <animate attributeName="width" from="0" to="820" dur="1.2s" begin="3.8s" fill="freeze" />
      </rect>
    </g>

    <!-- blinking cursor -->
    <rect x="620" y="70" width="6" height="60" rx="2" fill="#ffffff">
      <animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/>
      <!-- keep cursor visible only after reveal -->
      <set attributeName="visibility" to="visible" begin="3.6s" fill="freeze"/>
    </rect>

    <!-- smaller subtitle revealed slightly after -->
    <g opacity="0" transform="translate(0,0)">
      <text x="50" y="170" font-family="Inter, Roboto, sans-serif" font-size="18" fill="#d1d5db" opacity="0.95">
        Bangladesh-based dev building tools, tutorials, and visual workflows for creative coders.
      </text>
      <animateTransform attributeName="transform" type="translate" from="0,8" to="0,0" dur="0.6s" begin="4.2s" fill="freeze"/>
      <animate attributeName="opacity" from="0" to="1" dur="0.6s" begin="4.2s" fill="freeze"/>
    </g>

    <!-- micro sparkle dots that drift (looped) -->
    <g opacity="0.28" transform="translate(0,0)">
      <circle cx="1050" cy="30" r="2.5" fill="#fff">
        <animate attributeName="cy" dur="6s" values="30;18;30" repeatCount="indefinite"/>
        <animate attributeName="cx" dur="8s" values="1050;1120;1050" repeatCount="indefinite"/>
      </circle>
      <circle cx="1120" cy="70" r="1.8" fill="#fff">
        <animate attributeName="cy" dur="5s" values="70;60;70" repeatCount="indefinite"/>
        <animate attributeName="cx" dur="7s" values="1120;1060;1120" repeatCount="indefinite"/>
      </circle>
    </g>
  </svg>

  <!-- animated badges (using shields) -->
  <p>
    <img src="https://img.shields.io/badge/Status-Building%20Tools-orange?style=for-the-badge&logo=visual-studio-code" alt="status" />
    <img src="https://img.shields.io/badge/Focus-Linux%20%7C%20React%20%7C%20Python-blue?style=for-the-badge&logo=linux" alt="focus" />
    <img src="https://img.shields.io/badge/Tutorials-Video%20%26%20Docs-green?style=for-the-badge&logo=read-the-docs" alt="tutorials" />
  </p>
</div>

---

<!-- Content: keep the rest of your original sections. I condensed and polished wording and kept the structure. -->
<h2 align="left">💡 About Me</h2>
I'm a developer who blends code with clarity. I build systems, scripts, and branding assets that make tech feel intuitive and expressive — from Linux performance tweaks to playful frontend UI.

---

<h2 align="left">🚧 Current Projects</h2>
- **Code Moft** — creative coding hub for tutorials, branding, and community inspiration  
- **React App Setup Tool** — fast scaffolding for beginners and pros  
- **Zorin OS Optimization** — performance & visual polish for mid-range hardware  
- **System Scripts** — swap, DNS, font rendering, and dev-tool resets automation

---

<h2 align="left">🧠 Developer Focus</h2>
- Linux system administration & CLI tooling  
- React.js, Python and modern frontend workflows  
- Neon aesthetics, real coder imagery, and playful UX  
- Beginner-friendly docs and bite-sized video tutorials

---

<h2 align="left">🛠️ Tech Stack</h2>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg" height="28" />&nbsp;
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" height="28" />&nbsp;
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg" height="28" />&nbsp;
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg" height="28" />&nbsp;
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" height="28" />&nbsp;
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg" height="28" />

---

<h2 align="left">📊 GitHub Stats</h2>
<div align="left">
  <img src="https://github-readme-stats.vercel.app/api?username=mdadeel&show_icons=true&theme=dracula&hide_border=false" height="140"/>
  <img src="https://github-readme-stats.vercel.app/api/top-langs?username=mdadeel&layout=compact&langs_count=5&theme=dracula&hide_border=false" height="140"/>
</div>

---

<h2 align="left">📫 Connect with Me</h2>
[Instagram](https://www.instagram.com/shahnawas.adeel/) • [Facebook](https://www.facebook.com/badshahnawas.adeel/) • [LinkedIn](https://www.linkedin.com/in/shahnawasadee1/) • [Email](mailto:shahnawasadeel@gmail.com) • [GitHub](https://github.com/mdadeel)

