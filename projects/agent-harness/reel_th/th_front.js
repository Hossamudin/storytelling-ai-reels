      // --- hook: text behind Hossam
      tl.fromTo("#bt-ai", { opacity: 0, y: 120, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: "expo.out" }, 1.15);
      off("#bt-ai", 5.05);
      pop("#fr-cf", 4.0, 0.3); off("#fr-cf", 5.1);
      slam("#bt-ag", 7.78, 2.6); slam("#bt-hr", 8.2, 2.6); sh(8.3, 18);
      off("#bt-ag, #bt-hr", 8.75, 0.12);
      // --- model vs harness opinion
      show("#fr-l1", 16.4); mask("#fr-h1i", 16.5); show("#fr-h1", 16.45);
      show("#fr-h2", 18.3); mask("#fr-h2i", 18.35);
      off("#fr-l1, #fr-h1, #fr-h2", 19.3, 0.2);
      show("#fr-l3", 23.15); show("#fr-h3", 23.2); mask("#fr-h3i", 23.25); off("#fr-l3, #fr-h3", 25.0, 0.2);
      // --- SIGNATURE: the harness locks around Hossam (brackets behind his body), HARNESS rises behind his head
      [["#bk1-a", -300, -300], ["#bk1-b", 300, -300], ["#bk1-c", -300, 300], ["#bk1-d", 300, 300]].forEach(([s, x, y], i) => {
        tl.fromTo(s, { opacity: 0, x, y, scale: 1.6, filter: "blur(14px)" }, { opacity: 1, x: 0, y: 0, scale: 1, filter: "blur(0px)", duration: 0.26, ease: "expo.out" }, 40.05 + i * 0.04);
      });
      sh(40.25, 14);
      show("#fr-h4", 40.1); mask("#fr-h4i", 40.15); off("#fr-h4", 41.7, 0.2);
      tl.fromTo("#bt-hr2", { opacity: 0 }, { opacity: 1, duration: 0.01 }, 41.75);
      tl.fromTo("#bt-hr2i", { y: 260, opacity: 0, filter: "blur(10px)" }, { y: 0, opacity: 1, filter: "blur(0px)", duration: 0.6, ease: "expo.out" }, 41.75);
      tl.to("#bk1 .ah-brk", { opacity: 0, duration: 0.3 }, 42.35); off("#bt-hr2", 42.35, 0.3);
      show("#fr-h5", 42.45); mask("#fr-h5i", 42.5);
      pop("#fr-s1", 42.95); pop("#fr-s2", 43.15);
      off("#fr-h5, #fr-s1, #fr-s2", 46.8, 0.2);
      // --- benchmarks behind
      tl.fromTo("#bt-bm", { opacity: 0, y: 100 }, { opacity: 1, y: 0, duration: 0.6, ease: "expo.out" }, 49.95); off("#bt-bm", 52.15, 0.15);
      // --- source 01 name
      show("#fr-l6", 64.8); show("#fr-h6", 64.85); mask("#fr-h6i", 64.9); off("#fr-l6, #fr-h6", 66.4, 0.2);
      // --- myth (on camera: opinion)
      on("#fr-myth", 73.2); tl.fromTo("#fr-m2", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 74.8);
      tl.fromTo("#fr-msp", { strokeDasharray: 1, strokeDashoffset: 1 }, { strokeDashoffset: 0, duration: 0.35, ease: "power2.out" }, 75.85);
      pop("#fr-mx", 76.1, 0.2); tl.to("#fr-myth", { filter: "grayscale(0.9) brightness(0.6)", duration: 0.3 }, 76.0);
      off("#fr-myth", 76.55, 0.2);
      slam("#fr-st", 77.3); sh(77.4, 14); off("#fr-st", 77.85, 0.15);
      // --- cost differs
      show("#fr-h7", 84.4); mask("#fr-h7i", 84.45);
      show("#fr-h8", 87.4); mask("#fr-h8i", 87.45); tl.fromTo("#fr-b8", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power3.out" }, 87.7);
      off("#fr-h7, #fr-h8", 88.2, 0.15);
      // --- x2 behind Hossam
      show("#fr-h9", 120.5); mask("#fr-h9i", 120.55); off("#fr-h9", 123.3, 0.15);
      slam("#bt-x2", 123.42, 3); sh(123.5, 22, 8);
      show("#fr-h10", 123.55); mask("#fr-h10i", 123.6); tl.fromTo("#fr-b10", { scaleX: 0 }, { scaleX: 1, duration: 0.4, ease: "power3.out" }, 123.85);
      off("#bt-x2, #fr-h10", 124.25, 0.12);
      // --- sources in comments, updated live
      pop("#fr-cm", 132.95); tl.fromTo("#fr-cm svg", { y: -10 }, { y: 10, duration: 0.3, yoyo: true, repeat: 5, ease: "sine.inOut" }, 133.1);
      pop("#fr-up", 135.3); tl.fromTo("#fr-ref", { rotation: 0 }, { rotation: 720, duration: 2.0, ease: "power2.inOut" }, 135.4);
      off("#fr-cm, #fr-up", 137.8, 0.15);
      // --- investigate
      show("#fr-h11", 145.95); mask("#fr-h11i", 145.95);
      pop("#fr-c1", 146.9); pop("#fr-c2", 148.3); off("#fr-h11, #fr-c1, #fr-c2", 148.85, 0.12);
      // --- outro: brackets lock around Hossam again (callback), CTA, salam
      [["#bk1-a", -200, -200], ["#bk1-b", 200, -200], ["#bk1-c", -200, 200], ["#bk1-d", 200, 200]].forEach(([s, x, y], i) => {
        tl.fromTo(s, { opacity: 0, x, y }, { opacity: 1, x: 0, y: 0, duration: 0.3, ease: "expo.out", immediateRender: false }, 164.5 + i * 0.04);
      });
      show("#fr-o1", 165.4); mask("#fr-o1i", 165.45);
      pop("#fr-o2", 166.3); tl.fromTo("#fr-bell", { rotation: 0 }, { rotation: 18, duration: 0.08, yoyo: true, repeat: 7, ease: "sine.inOut" }, 166.6);
      on("#fr-cb", 167.1, 30);
      tl.fromTo("#fr-car", { opacity: 1 }, { opacity: 0.15, duration: 0.25, ease: "steps(1)", yoyo: true, repeat: 9 }, 167.1);
      { const el = document.getElementById("fr-tt"), txt = "اكتب سؤالك هنا…", p = { n: 0 }; el.textContent = "";
        tl.fromTo(p, { n: 0 }, { n: txt.length, duration: txt.length / 16, ease: "none", onUpdate: () => (el.textContent = txt.slice(0, Math.round(p.n))) }, 167.4); }
      off("#fr-cb", 169.5, 0.2);
      show("#fr-bye", 169.65); mask("#fr-byei", 169.7);
      tl.to("#thw, #front", { opacity: 0, duration: 0.5 }, 170.95);
