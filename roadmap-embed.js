// Keeps the embedded product roadmap (release-notes/roadmap.mdx) on the same
// theme as the docs. Mintlify toggles a `dark` class on <html>; the app page
// inside the iframe applies the theme it is told about via postMessage.
(function () {
  var APP_ORIGIN = "https://app.msportal.ai";
  var MESSAGE_TYPE = "msportal-roadmap-theme";

  function currentTheme() {
    return document.documentElement.classList.contains("dark") ? "dark" : "light";
  }

  function frames() {
    return Array.prototype.slice.call(
      document.querySelectorAll("iframe[data-roadmap-embed]"),
    );
  }

  function post(frame) {
    if (!frame.contentWindow) return;
    try {
      frame.contentWindow.postMessage(
        { type: MESSAGE_TYPE, theme: currentTheme() },
        APP_ORIGIN,
      );
    } catch (error) {
      /* frame not ready yet; the load listener posts again */
    }
  }

  function withTheme(src) {
    try {
      var url = new URL(src, window.location.href);
      url.searchParams.set("theme", currentTheme());
      return url.toString();
    } catch (error) {
      return src;
    }
  }

  // Frames found after a client-side navigation have not started loading in
  // earnest yet, so the theme goes on the URL and paints right the first time.
  // Frames present at page load are already loading; they get the message.
  function attach(frame, fresh) {
    if (frame.dataset.roadmapEmbedReady) return;
    frame.dataset.roadmapEmbedReady = "1";
    frame.addEventListener("load", function () {
      post(frame);
    });
    if (fresh) {
      frame.src = withTheme(frame.getAttribute("src") || "");
    } else {
      post(frame);
    }
  }

  frames().forEach(function (frame) {
    attach(frame, false);
  });

  new MutationObserver(function () {
    frames().forEach(post);
  }).observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["class"],
  });

  var scheduled = false;
  new MutationObserver(function () {
    if (scheduled) return;
    scheduled = true;
    window.requestAnimationFrame(function () {
      scheduled = false;
      frames().forEach(function (frame) {
        attach(frame, true);
      });
    });
  }).observe(document.body, { childList: true, subtree: true });
})();
