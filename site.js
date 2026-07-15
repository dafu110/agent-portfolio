(() => {
  const toggle = document.querySelector(".nav-toggle");
  const nav = document.querySelector("#site-nav");
  const header = document.querySelector(".site-header");
  const desktop = window.matchMedia("(min-width: 981px)");

  if (!toggle || !nav) return;

  const isOpen = () => toggle.getAttribute("aria-expanded") === "true";

  const close = ({ restoreFocus = false } = {}) => {
    toggle.setAttribute("aria-expanded", "false");
    nav.dataset.open = "false";
    if (restoreFocus && !desktop.matches) toggle.focus();
  };

  toggle.addEventListener("click", () => {
    const open = !isOpen();
    toggle.setAttribute("aria-expanded", String(open));
    nav.dataset.open = String(open);
  });

  nav.addEventListener("click", (event) => {
    if (event.target instanceof HTMLAnchorElement) close();
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && isOpen()) {
      close({ restoreFocus: true });
    }
  });

  document.addEventListener("pointerdown", (event) => {
    if (isOpen() && header && !header.contains(event.target)) close();
  });

  desktop.addEventListener("change", () => close());

  const demoLink = document.querySelector('a[href="#peopleops-demo"]');
  const demoDisclosure = document.querySelector("#peopleops-demo");
  demoLink?.addEventListener("click", () => {
    if (demoDisclosure instanceof HTMLDetailsElement) demoDisclosure.open = true;
  });

  document.querySelectorAll(".video-disclosure").forEach((disclosure) => {
    disclosure.addEventListener("toggle", () => {
      if (!disclosure.open) disclosure.querySelector("video")?.pause();
    });
  });

  document.querySelectorAll(".demo-video-frame").forEach((frame) => {
    const video = frame.querySelector("video");
    const button = frame.querySelector(".demo-video-toggle");
    if (!(video instanceof HTMLVideoElement) || !(button instanceof HTMLButtonElement)) return;

    const label = video.getAttribute("aria-label") || "演示视频";
    const buttonLabel = button.querySelector("span");
    const sync = () => {
      const playing = !video.paused && !video.ended;
      frame.dataset.state = playing ? "playing" : "paused";
      button.setAttribute("aria-label", `${playing ? "暂停" : "播放"} ${label}`);
      if (buttonLabel) buttonLabel.textContent = playing ? "暂停" : "播放";
    };
    const togglePlayback = () => {
      if (video.paused || video.ended) video.play().catch(sync);
      else video.pause();
    };

    button.addEventListener("click", togglePlayback);
    video.addEventListener("click", togglePlayback);
    video.addEventListener("play", sync);
    video.addEventListener("pause", sync);
    video.addEventListener("ended", sync);
    sync();
  });
})();
