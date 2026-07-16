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

  const contactDialog = document.querySelector("[data-contact-dialog]");
  const contactPanel = contactDialog?.querySelector(".contact-panel");
  const contactStatus = contactDialog?.querySelector("[data-contact-status]");
  const emailTarget = contactDialog?.querySelector("[data-contact-email]");
  const copyEmailButton = contactDialog?.querySelector("[data-copy-email]");
  let contactReturnTarget = null;

  const copyToClipboard = async (text) => {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
      return;
    }

    const field = document.createElement("textarea");
    field.value = text;
    field.setAttribute("readonly", "");
    field.style.position = "fixed";
    field.style.opacity = "0";
    document.body.append(field);
    field.select();
    document.execCommand("copy");
    field.remove();
  };

  const openContact = (trigger) => {
    if (!(contactDialog instanceof HTMLElement)) return;
    contactReturnTarget = trigger instanceof HTMLElement ? trigger : null;
    contactDialog.hidden = false;
    document.body.style.overflow = "hidden";
    if (contactStatus) contactStatus.textContent = "";
    if (contactPanel instanceof HTMLElement) contactPanel.focus();
  };

  const closeContact = ({ restoreFocus = false } = {}) => {
    if (!(contactDialog instanceof HTMLElement) || contactDialog.hidden) return;
    contactDialog.hidden = true;
    document.body.style.overflow = "";
    if (contactStatus) contactStatus.textContent = "";
    if (restoreFocus) contactReturnTarget?.focus();
  };

  document.querySelectorAll("[data-contact-open]").forEach((trigger) => {
    trigger.addEventListener("click", () => openContact(trigger));
  });

  contactDialog?.querySelectorAll("[data-contact-close]").forEach((trigger) => {
    trigger.addEventListener("click", () => closeContact({ restoreFocus: true }));
  });

  copyEmailButton?.addEventListener("click", async () => {
    const email = emailTarget?.textContent?.trim();
    if (!email) return;

    try {
      await copyToClipboard(email);
      if (contactStatus) contactStatus.textContent = "邮箱已复制，可以直接粘贴发送。";
    } catch (_error) {
      if (contactStatus) contactStatus.textContent = `复制失败，请手动复制：${email}`;
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeContact({ restoreFocus: true });
  });
})();
