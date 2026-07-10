(function () {
  "use strict";

  var root = document.documentElement;
  root.classList.add("js");

  var MOBILE_QUERY = "(max-width: 63.999rem)";
  var FOCUSABLE_SELECTOR = [
    "a[href]",
    "button:not([disabled])",
    "input:not([disabled])",
    "select:not([disabled])",
    "textarea:not([disabled])",
    "[tabindex]:not([tabindex='-1'])"
  ].join(",");

  function fragmentTarget(href) {
    if (!href || href.charAt(0) !== "#" || href === "#") {
      return null;
    }

    try {
      return document.getElementById(decodeURIComponent(href.slice(1)));
    } catch (_error) {
      return null;
    }
  }

  function visibleFocusableElements(container) {
    return Array.prototype.slice.call(container.querySelectorAll(FOCUSABLE_SELECTOR)).filter(function (element) {
      return !element.hidden && element.getAttribute("aria-hidden") !== "true" && element.getClientRects().length > 0;
    });
  }

  function focusFragment(target) {
    if (!target) {
      return;
    }

    var suppliedTabIndex = target.hasAttribute("tabindex");
    if (!suppliedTabIndex) {
      target.setAttribute("tabindex", "-1");
    }

    target.focus({ preventScroll: true });

    if (!suppliedTabIndex) {
      target.addEventListener("blur", function removeTemporaryTabIndex() {
        target.removeAttribute("tabindex");
      }, { once: true });
    }
  }

  function initSceneDrawer() {
    var nav = document.querySelector("[data-scene-nav], .scene-nav");
    var toggle = document.querySelector("[data-scene-nav-toggle], .scene-nav-toggle");
    var scrim = document.querySelector("[data-scene-nav-scrim], .scene-nav-scrim");

    if (!nav || !toggle) {
      return nav;
    }

    var media = window.matchMedia(MOBILE_QUERY);
    var isOpen = false;
    var lastFocused = null;
    var inertRecords = [];
    var openLabel = toggle.getAttribute("data-label-open") || toggle.getAttribute("aria-label") || "Szenen öffnen";
    var closeLabel = toggle.getAttribute("data-label-close") || "Szenen schließen";
    var originalRole = nav.getAttribute("role");
    var originalAriaModal = nav.getAttribute("aria-modal");

    if (!nav.id) {
      nav.id = "scene-nav";
    }

    toggle.setAttribute("type", "button");
    toggle.setAttribute("aria-controls", nav.id);
    toggle.setAttribute("aria-expanded", "false");

    if (!nav.hasAttribute("aria-label") && !nav.hasAttribute("aria-labelledby")) {
      var navTitle = nav.querySelector("[data-scene-nav-title], h2");
      if (navTitle) {
        if (!navTitle.id) {
          navTitle.id = nav.id + "-title";
        }
        nav.setAttribute("aria-labelledby", navTitle.id);
      } else {
        nav.setAttribute("aria-label", "Szenen");
      }
    }

    if (scrim) {
      if (scrim.tagName === "BUTTON") {
        scrim.setAttribute("type", "button");
      }
      if (!scrim.hasAttribute("aria-label")) {
        scrim.setAttribute("aria-label", "Szenennavigation schließen");
      }
      scrim.setAttribute("aria-hidden", "true");
      scrim.setAttribute("tabindex", "-1");
    }

    function backgroundTargets() {
      var explicit = Array.prototype.slice.call(document.querySelectorAll("[data-drawer-inert]"));
      var candidates = explicit.length
        ? explicit
        : Array.prototype.slice.call(document.querySelectorAll("main, .site-footer"));

      return candidates.filter(function (element, index, list) {
        return list.indexOf(element) === index &&
          element !== nav &&
          !element.contains(nav) &&
          !element.contains(toggle);
      });
    }

    function setBackgroundInactive(inactive) {
      if (inactive) {
        inertRecords = backgroundTargets().map(function (element) {
          var record = {
            element: element,
            hadInert: element.hasAttribute("inert"),
            ariaHidden: element.getAttribute("aria-hidden")
          };

          element.setAttribute("inert", "");
          element.setAttribute("aria-hidden", "true");
          return record;
        });
        return;
      }

      inertRecords.forEach(function (record) {
        if (!record.hadInert) {
          record.element.removeAttribute("inert");
        }

        if (record.ariaHidden === null) {
          record.element.removeAttribute("aria-hidden");
        } else {
          record.element.setAttribute("aria-hidden", record.ariaHidden);
        }
      });
      inertRecords = [];
    }

    function renderState() {
      var mobile = media.matches;

      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
      toggle.setAttribute("aria-label", isOpen ? closeLabel : openLabel);
      nav.setAttribute("data-open", isOpen ? "true" : "false");

      if (mobile) {
        nav.setAttribute("aria-hidden", isOpen ? "false" : "true");
        if (isOpen) {
          nav.setAttribute("role", "dialog");
          nav.setAttribute("aria-modal", "true");
        } else {
          nav.removeAttribute("aria-modal");
        }
      } else {
        nav.removeAttribute("aria-hidden");
        if (originalRole === null) {
          nav.removeAttribute("role");
        } else {
          nav.setAttribute("role", originalRole);
        }
        if (originalAriaModal === null) {
          nav.removeAttribute("aria-modal");
        } else {
          nav.setAttribute("aria-modal", originalAriaModal);
        }
      }

      if (scrim) {
        scrim.setAttribute("aria-hidden", isOpen ? "false" : "true");
      }

      if (isOpen) {
        document.body.setAttribute("data-scene-nav-open", "true");
      } else {
        document.body.removeAttribute("data-scene-nav-open");
      }
    }

    function openDrawer() {
      if (!media.matches || isOpen) {
        return;
      }

      lastFocused = document.activeElement;
      isOpen = true;
      setBackgroundInactive(true);
      renderState();

      window.requestAnimationFrame(function () {
        var focusable = visibleFocusableElements(nav);
        if (focusable.length) {
          focusable[0].focus();
        } else {
          nav.setAttribute("tabindex", "-1");
          nav.focus();
        }
      });
    }

    function closeDrawer(options) {
      var settings = options || {};
      var wasOpen = isOpen;

      isOpen = false;
      setBackgroundInactive(false);
      renderState();

      if (wasOpen && settings.restoreFocus !== false) {
        var focusTarget = lastFocused && document.contains(lastFocused) ? lastFocused : toggle;
        focusTarget.focus({ preventScroll: true });
      }
    }

    function trapFocus(event) {
      if (!isOpen || event.key !== "Tab") {
        return;
      }

      var focusable = visibleFocusableElements(nav);
      if (!focusable.length) {
        event.preventDefault();
        nav.focus();
        return;
      }

      var first = focusable[0];
      var last = focusable[focusable.length - 1];

      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    toggle.addEventListener("click", function () {
      if (isOpen) {
        closeDrawer();
      } else {
        openDrawer();
      }
    });

    if (scrim) {
      scrim.addEventListener("click", function () {
        closeDrawer();
      });
    }

    nav.addEventListener("keydown", trapFocus);

    nav.addEventListener("click", function (event) {
      var link = event.target.closest("a");
      if (!link || !media.matches) {
        return;
      }

      var target = fragmentTarget(link.getAttribute("href"));
      closeDrawer({ restoreFocus: !target });

      if (target) {
        window.setTimeout(function () {
          focusFragment(target);
        }, 0);
      }
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && isOpen) {
        event.preventDefault();
        closeDrawer();
      }
    });

    function syncViewportMode() {
      if (!media.matches && isOpen) {
        closeDrawer({ restoreFocus: false });
      } else {
        renderState();
      }
    }

    if (typeof media.addEventListener === "function") {
      media.addEventListener("change", syncViewportMode);
    } else {
      media.addListener(syncViewportMode);
    }

    renderState();
    return nav;
  }

  function initScrollSpy(nav) {
    if (!nav) {
      return;
    }

    var links = Array.prototype.slice.call(nav.querySelectorAll("a[href^='#']"));
    var pairs = links.map(function (link) {
      var target = fragmentTarget(link.getAttribute("href"));
      return target ? { link: link, target: target } : null;
    }).filter(Boolean);

    var scenePairs = pairs.filter(function (pair) {
      return pair.link.hasAttribute("data-scene-link") || pair.target.matches(".scene, [data-scene]");
    });

    if (!scenePairs.length) {
      return;
    }

    var activeId = null;
    var sceneLinks = scenePairs.map(function (pair) { return pair.link; });
    var targets = scenePairs.map(function (pair) { return pair.target; });
    var linkById = new Map(scenePairs.map(function (pair) {
      return [pair.target.id, pair.link];
    }));

    function keepLinkVisible(link) {
      var navRect = nav.getBoundingClientRect();
      var linkRect = link.getBoundingClientRect();
      var upperEdge = navRect.top + 48;
      var lowerEdge = navRect.bottom - 32;

      if (linkRect.top < upperEdge) {
        nav.scrollTop -= upperEdge - linkRect.top;
      } else if (linkRect.bottom > lowerEdge) {
        nav.scrollTop += linkRect.bottom - lowerEdge;
      }
    }

    function notifySceneChange(target) {
      document.dispatchEvent(new CustomEvent("screenplay:scenechange", {
        detail: { id: target.id }
      }));
    }

    function setActive(target) {
      if (!target || !target.id) {
        return;
      }

      if (target.id === activeId) {
        notifySceneChange(target);
        return;
      }

      var activeLink = linkById.get(target.id);
      if (!activeLink) {
        return;
      }

      activeId = target.id;

      sceneLinks.forEach(function (link) {
        var active = link === activeLink;
        link.classList.toggle("is-active", active);
        if (active) {
          link.setAttribute("aria-current", "location");
        } else {
          link.removeAttribute("aria-current");
        }
      });

      links.forEach(function (link) {
        link.classList.remove("is-active-act");
      });

      var actId = target.getAttribute("data-act");
      if (!actId) {
        var act = target.closest(".act-block[id], [data-act-block][id]");
        actId = act ? act.id : null;
      }

      if (actId) {
        links.forEach(function (link) {
          if (link.getAttribute("href") === "#" + actId) {
            link.classList.add("is-active-act");
          }
        });
      }

      keepLinkVisible(activeLink);
      notifySceneChange(target);
    }

    function activeTargetFromGeometry() {
      var marker = Math.min(window.innerHeight * 0.32, 260);
      var candidate = targets[0];

      for (var index = 0; index < targets.length; index += 1) {
        var target = targets[index];
        if (target.getBoundingClientRect().top <= marker) {
          candidate = target;
        } else {
          break;
        }
      }

      var pageBottom = window.scrollY + window.innerHeight;
      var documentBottom = document.documentElement.scrollHeight - 2;
      if (pageBottom >= documentBottom) {
        candidate = targets[targets.length - 1];
      }

      return candidate;
    }

    function updateFromGeometry() {
      setActive(activeTargetFromGeometry());
    }

    if ("IntersectionObserver" in window) {
      var observer = new IntersectionObserver(function () {
        updateFromGeometry();
      }, {
        root: null,
        rootMargin: "-18% 0px -68% 0px",
        threshold: [0, 0.01]
      });

      targets.forEach(function (target) {
        observer.observe(target);
      });
    } else {
      var ticking = false;
      window.addEventListener("scroll", function () {
        if (ticking) {
          return;
        }
        ticking = true;
        window.requestAnimationFrame(function () {
          updateFromGeometry();
          ticking = false;
        });
      }, { passive: true });
    }

    window.addEventListener("hashchange", function () {
      var target = fragmentTarget(window.location.hash);
      if (target && linkById.has(target.id)) {
        setActive(target);
      } else {
        updateFromGeometry();
      }
    });

    var hashTarget = fragmentTarget(window.location.hash);
    if (hashTarget && linkById.has(hashTarget.id)) {
      setActive(hashTarget);
    } else {
      window.requestAnimationFrame(updateFromGeometry);
    }
  }

  function initReadingProgress() {
    var progress = document.querySelector("[data-reading-progress], .reading-progress");
    var screenplay = document.querySelector("[data-screenplay], .screenplay");

    if (!progress || !screenplay) {
      return;
    }

    var ticking = false;

    function update() {
      var rect = screenplay.getBoundingClientRect();
      var start = window.scrollY + rect.top;
      var end = start + screenplay.offsetHeight - window.innerHeight;
      var ratio = end > start ? (window.scrollY - start) / (end - start) : 1;
      var value = Math.max(0, Math.min(1, ratio));

      if (progress.tagName === "PROGRESS") {
        progress.max = 100;
        progress.value = Math.round(value * 100);
      } else {
        progress.setAttribute("role", "progressbar");
        progress.setAttribute("aria-valuemin", "0");
        progress.setAttribute("aria-valuemax", "100");
        progress.style.setProperty("--reading-progress", String(value));
        progress.setAttribute("aria-valuenow", String(Math.round(value * 100)));
      }

      ticking = false;
    }

    function requestUpdate() {
      if (ticking) {
        return;
      }
      ticking = true;
      window.requestAnimationFrame(update);
    }

    window.addEventListener("scroll", requestUpdate, { passive: true });
    window.addEventListener("resize", requestUpdate);
    window.addEventListener("hashchange", requestUpdate);
    window.addEventListener("load", requestUpdate, { once: true });
    document.addEventListener("screenplay:scenechange", requestUpdate);

    Array.prototype.slice.call(screenplay.querySelectorAll("img")).forEach(function (image) {
      if (!image.complete) {
        image.addEventListener("load", requestUpdate, { once: true });
      }
    });

    requestUpdate();
  }

  function init() {
    var nav = initSceneDrawer() || document.querySelector("[data-scene-nav], .scene-nav");
    initScrollSpy(nav);
    initReadingProgress();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init, { once: true });
  } else {
    init();
  }
}());
