/**
 * ShopStyle — Main JavaScript
 * Runs after DOM + Bootstrap are loaded.
 * Step 1: Core UI behaviours (loader, navbar, toasts, back-to-top, search).
 */

"use strict";

/* ============================================================
   1. PAGE LOADER
============================================================ */
(function initLoader() {
    const loader = document.getElementById("pageLoader");
    if (!loader) return;

    // Hide once window resources are ready
    window.addEventListener("load", () => {
        setTimeout(() => {
            loader.classList.add("hidden");
        }, 300); // small grace period so content settles
    });

    // Safety net: force-hide after 4 s in case load event stalls
    setTimeout(() => loader.classList.add("hidden"), 4000);
}());


/* ============================================================
   2. STICKY NAVBAR — add shadow on scroll
============================================================ */
(function initNavbar() {
    const navbar = document.getElementById("mainNavbar");
    if (!navbar) return;

    const handler = () => {
        navbar.classList.toggle("scrolled", window.scrollY > 10);
    };

    window.addEventListener("scroll", handler, { passive: true });
    handler(); // run once on page load
}());


/* ============================================================
   3. BACK-TO-TOP BUTTON
============================================================ */
(function initBackToTop() {
    const btn = document.getElementById("backToTop");
    if (!btn) return;

    window.addEventListener(
        "scroll",
        () => btn.classList.toggle("visible", window.scrollY > 400),
        { passive: true }
    );

    btn.addEventListener("click", () => {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}());


/* ============================================================
   4. TOAST HELPER — call window.showToast(msg, type)
   type: 'success' | 'error' | 'warning' | 'info'
============================================================ */
(function initToastHelper() {
    /**
     * Show a programmatic Bootstrap Toast.
     * @param {string} message - Text to display.
     * @param {'success'|'error'|'warning'|'info'} type - Visual style.
     * @param {number} [delay=4000] - Auto-hide delay in ms.
     */
    window.showToast = function showToast(message, type = "info", delay = 4000) {
        const config = {
            success: { icon: "fa-check-circle",       color: "#10b981", cls: "msg-success" },
            error:   { icon: "fa-times-circle",       color: "#FF3F6C", cls: "msg-error"   },
            warning: { icon: "fa-exclamation-triangle",color: "#f59e0b", cls: "msg-warning" },
            info:    { icon: "fa-info-circle",        color: "#3b82f6", cls: "msg-info"    },
        };
        const { icon, color, cls } = config[type] || config.info;

        // Ensure the toast container exists
        let container = document.querySelector(".toast-container");
        if (!container) {
            container = document.createElement("div");
            container.className =
                "toast-container position-fixed top-0 end-0 p-3";
            container.style.zIndex = "1090";
            document.body.appendChild(container);
        }

        // Build toast element
        const toast = document.createElement("div");
        toast.className = `toast msg-toast ${cls}`;
        toast.setAttribute("role", "alert");
        toast.setAttribute("aria-live", "assertive");
        toast.setAttribute("aria-atomic", "true");
        toast.innerHTML = `
            <div class="toast-body d-flex align-items-start gap-3">
                <i class="fas ${icon} mt-1" style="color:${color};font-size:1.15rem;flex-shrink:0;"></i>
                <span class="flex-grow-1 fw-semibold" style="font-size:.875rem;">${message}</span>
                <button type="button" class="btn-close btn-close-sm flex-shrink-0"
                        data-bs-dismiss="toast" aria-label="Close"></button>
            </div>`;

        container.appendChild(toast);

        // Bootstrap Toast instance
        const bsToast = new bootstrap.Toast(toast, {
            autohide: true,
            delay: delay,
        });
        bsToast.show();

        // Remove from DOM once hidden
        toast.addEventListener("hidden.bs.toast", () => toast.remove());
    };
}());


/* ============================================================
   5. AUTO-INITIALISE EXISTING DJANGO TOASTS
   (rendered by messages.html on page load)
============================================================ */
(function autoShowToasts() {
    document.querySelectorAll(".toast.msg-toast").forEach((el) => {
        const toast = bootstrap.Toast.getOrCreateInstance(el, {
            autohide: true,
            delay: parseInt(el.dataset.bsDelay || "4500", 10),
        });
        toast.show();
    });
}());


/* ============================================================
   6. NAVBAR SEARCH — live suggestions (stub)
   Real API endpoint wired in Step 4 (Products App).
============================================================ */
(function initNavSearch() {
    const input    = document.getElementById("navSearchInput");
    const dropdown = document.getElementById("searchDropdown");
    if (!input || !dropdown) return;

    let debounceTimer = null;

    input.addEventListener("input", function () {
        clearTimeout(debounceTimer);
        const q = this.value.trim();

        if (q.length < 2) {
            closeDropdown();
            return;
        }

        debounceTimer = setTimeout(() => fetchSuggestions(q), 280);
    });

    input.addEventListener("focus", function () {
        if (this.value.trim().length >= 2) {
            dropdown.classList.add("open");
        }
    });

    // Close dropdown when clicking outside
    document.addEventListener("click", (e) => {
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
            closeDropdown();
        }
    });

    /**
     * Fetch search suggestions from the backend.
     * Step 4 adds the real endpoint; until then this shows a placeholder.
     */
    async function fetchSuggestions(query) {
        try {
            const res = await fetch(
                `/products/search/?q=${encodeURIComponent(query)}&format=json`,
                { headers: { "X-Requested-With": "XMLHttpRequest" } }
            );

            if (!res.ok) throw new Error("Search API not ready");

            const data = await res.json();
            renderDropdown(data.results || [], query);
        } catch {
            // Step 4 not built yet — show a friendly placeholder
            renderDropdown([], query, true);
        }
    }

    function renderDropdown(results, query, isPlaceholder = false) {
        if (isPlaceholder) {
            dropdown.innerHTML = `
                <div class="search-dd-item text-muted" style="font-size:.8rem;">
                    <i class="fas fa-search"></i>
                    Press Enter to search for "<strong>${escapeHtml(query)}</strong>"
                </div>`;
        } else if (results.length === 0) {
            dropdown.innerHTML = `
                <div class="search-dd-item text-muted" style="font-size:.8rem;">
                    <i class="fas fa-face-meh"></i>
                    No results for "${escapeHtml(query)}"
                </div>`;
        } else {
            dropdown.innerHTML = results
                .map(
                    (r) => `
                    <a href="${r.url}" class="search-dd-item">
                        <i class="fas fa-${r.type === "product" ? "tag" : "folder"}"></i>
                        ${escapeHtml(r.name)}
                        ${r.price ? `<span class="ms-auto text-muted small">₹${r.price}</span>` : ""}
                    </a>`
                )
                .join("");
        }
        dropdown.classList.add("open");
    }

    function closeDropdown() {
        dropdown.classList.remove("open");
    }

    function escapeHtml(str) {
        return str.replace(/[&<>"']/g, (c) => ({
            "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;",
        })[c]);
    }

    // Close on Escape
    input.addEventListener("keydown", (e) => {
        if (e.key === "Escape") { closeDropdown(); input.blur(); }
    });
}());


/* ============================================================
   7. CSRF TOKEN HELPER — attach to all AJAX POST requests
============================================================ */
(function initCsrf() {
    /**
     * Read CSRF token from cookie.
     * @param {string} name - Cookie name.
     * @returns {string|null}
     */
    function getCookie(name) {
        const match = document.cookie.match(
            new RegExp("(?:^|; )" + name.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + "=([^;]*)")
        );
        return match ? decodeURIComponent(match[1]) : null;
    }

    /**
     * Convenience wrapper around fetch() that automatically
     * includes Django's CSRF token for state-changing requests.
     *
     * Usage:
     *   const data = await window.ajax('/cart/add/', {product_id: 5, qty: 1});
     *
     * @param {string} url
     * @param {object} body - JSON-serialisable data.
     * @param {'POST'|'PUT'|'PATCH'|'DELETE'} [method='POST']
     * @returns {Promise<object>}
     */
    window.ajax = async function ajax(url, body = {}, method = "POST") {
        const response = await fetch(url, {
            method,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken") || "",
                "X-Requested-With": "XMLHttpRequest",
            },
            body: method !== "GET" ? JSON.stringify(body) : undefined,
        });

        const contentType = response.headers.get("content-type") || "";
        if (contentType.includes("application/json")) {
            return response.json();
        }
        return { ok: response.ok, status: response.status };
    };
}());


/* ============================================================
   8. SMOOTH REVEAL — fade-in elements when they enter viewport
============================================================ */
(function initReveal() {
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("revealed");
                    observer.unobserve(entry.target);
                }
            });
        },
        { threshold: 0.08, rootMargin: "0px 0px -40px 0px" }
    );

    // Add reveal CSS to <head> once
    const style = document.createElement("style");
    style.textContent = `
        .reveal-on-scroll {
            opacity: 0;
            transform: translateY(24px);
            transition: opacity .5s ease, transform .5s ease;
        }
        .reveal-on-scroll.revealed {
            opacity: 1;
            transform: translateY(0);
        }`;
    document.head.appendChild(style);

    // Observe all elements with the class
    document.querySelectorAll(".reveal-on-scroll").forEach((el) =>
        observer.observe(el)
    );
}());


/* ============================================================
   9. MOBILE SEARCH — inject search bar below navbar on mobile
============================================================ */
(function initMobileSearch() {
    // Only show on narrow screens
    if (window.innerWidth >= 992) return;

    const navbar = document.getElementById("mainNavbar");
    if (!navbar) return;

    const mobileSearchBar = document.createElement("div");
    mobileSearchBar.className = "mobile-search-bar bg-white px-3 py-2 border-bottom";
    mobileSearchBar.innerHTML = `
        <form action="/products/search/" method="get" class="d-flex" autocomplete="off">
            <div class="nav-search-wrapper w-100">
                <i class="fas fa-search nav-search-icon"></i>
                <input class="nav-search-input w-100"
                       type="search" name="q"
                       placeholder="Search brands, products &amp; more">
            </div>
        </form>`;

    navbar.insertAdjacentElement("afterend", mobileSearchBar);
}());


/* ============================================================
   10. WISHLIST / CART BUTTON — add spinner on click (UX)
============================================================ */
document.addEventListener("click", function (e) {
    const btn = e.target.closest("[data-ajax-btn]");
    if (!btn) return;

    const icon = btn.querySelector("i");
    if (!icon) return;

    const originalClass = icon.className;
    icon.className = "fas fa-spinner fa-spin";
    btn.disabled = true;

    // Re-enable after 3 s (the real handler resolves faster)
    setTimeout(() => {
        icon.className = originalClass;
        btn.disabled = false;
    }, 3000);
});


/* ============================================================
   11. QUANTITY STEPPER — generic +/- counter for forms
============================================================ */
document.addEventListener("click", function (e) {
    const btn = e.target.closest("[data-qty-btn]");
    if (!btn) return;

    const targetId = btn.dataset.qtyBtn;
    const input = document.getElementById(targetId);
    if (!input) return;

    const min = parseInt(input.min || "1", 10);
    const max = parseInt(input.max || "999", 10);
    let val = parseInt(input.value || "1", 10);

    if (btn.dataset.dir === "up")   val = Math.min(val + 1, max);
    if (btn.dataset.dir === "down") val = Math.max(val - 1, min);

    input.value = val;
    input.dispatchEvent(new Event("change", { bubbles: true }));
});







"use strict";

/* ============================================================
   1. PAGE LOADER — hides after page loads
============================================================ */
(function initLoader() {
    var loader = document.getElementById("pageLoader");
    if (!loader) return;

    function hide() {
        loader.classList.add("hidden");
    }

    // Hide after DOM + assets are ready
    if (document.readyState === "complete") {
        setTimeout(hide, 300);
    } else {
        window.addEventListener("load", function () {
            setTimeout(hide, 300);
        });
    }

    // Absolute safety net — force hide after 3 s
    setTimeout(hide, 3000);
}());


/* ============================================================
   2. STICKY NAVBAR — add shadow class on scroll
============================================================ */
(function initNavbar() {
    var navbar = document.getElementById("mainNavbar");
    if (!navbar) return;

    function onScroll() {
        if (window.scrollY > 10) {
            navbar.classList.add("scrolled");
        } else {
            navbar.classList.remove("scrolled");
        }
    }

    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
}());


/* ============================================================
   3. BACK-TO-TOP BUTTON
============================================================ */
(function initBackToTop() {
    var btn = document.getElementById("backToTop");
    if (!btn) return;

    window.addEventListener("scroll", function () {
        if (window.scrollY > 400) {
            btn.classList.add("visible");
        } else {
            btn.classList.remove("visible");
        }
    }, { passive: true });

    btn.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });
}());


/* ============================================================
   4. AUTO-SHOW DJANGO TOASTS (from messages.html)
============================================================ */
(function autoShowToasts() {
    document.querySelectorAll(".toast.msg-toast").forEach(function (el) {
        var toast = bootstrap.Toast.getOrCreateInstance(el, {
            autohide: true,
            delay: parseInt(el.getAttribute("data-bs-delay") || "4500", 10),
        });
        toast.show();
    });
}());


/* ============================================================
   5. TOAST HELPER — window.showToast('message', 'success')
   Types: 'success' | 'error' | 'warning' | 'info'
============================================================ */
(function initToastHelper() {
    window.showToast = function (message, type, delay) {
        type  = type  || "info";
        delay = delay || 4000;

        var configs = {
            success: { icon: "fa-check-circle",        cls: "msg-success" },
            error:   { icon: "fa-times-circle",        cls: "msg-error"   },
            warning: { icon: "fa-exclamation-triangle", cls: "msg-warning" },
            info:    { icon: "fa-info-circle",         cls: "msg-info"    },
        };
        var cfg = configs[type] || configs.info;

        // Find or create the toast container
        var container = document.querySelector(".toast-container");
        if (!container) {
            container = document.createElement("div");
            container.className = "toast-container position-fixed top-0 end-0 p-3";
            container.style.zIndex = "1090";
            document.body.appendChild(container);
        }

        // Build the toast element
        var toast = document.createElement("div");
        toast.className = "toast msg-toast " + cfg.cls;
        toast.setAttribute("role", "alert");
        toast.setAttribute("aria-live", "assertive");
        toast.setAttribute("aria-atomic", "true");
        toast.innerHTML =
            '<div class="toast-body d-flex align-items-start gap-3">' +
                '<i class="fas ' + cfg.icon + ' msg-icon mt-1 flex-shrink-0"></i>' +
                '<span class="flex-grow-1 fw-semibold msg-text">' + message + '</span>' +
                '<button type="button" class="btn-close btn-close-sm flex-shrink-0" ' +
                        'data-bs-dismiss="toast" aria-label="Close"></button>' +
            '</div>';

        container.appendChild(toast);

        var bsToast = new bootstrap.Toast(toast, {
            autohide: true,
            delay: delay,
        });
        bsToast.show();

        toast.addEventListener("hidden.bs.toast", function () {
            toast.remove();
        });
    };
}());


/* ============================================================
   6. CSRF HELPER — window.ajax('/url/', {data}, 'POST')
============================================================ */
(function initCsrf() {
    function getCookie(name) {
        var match = document.cookie.match(
            new RegExp("(?:^|; )" + name + "=([^;]*)")
        );
        return match ? decodeURIComponent(match[1]) : null;
    }

    window.ajax = async function (url, body, method) {
        body   = body   || {};
        method = method || "POST";

        var response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type":     "application/json",
                "X-CSRFToken":      getCookie("csrftoken") || "",
                "X-Requested-With": "XMLHttpRequest",
            },
            body: method !== "GET" ? JSON.stringify(body) : undefined,
        });

        var ct = response.headers.get("content-type") || "";
        if (ct.includes("application/json")) {
            return response.json();
        }
        return { ok: response.ok, status: response.status };
    };
}());


/* ============================================================
   7. NAVBAR LIVE SEARCH (stub — wired to real API in Step 4)
============================================================ */
(function initNavSearch() {
    var input    = document.getElementById("navSearchInput");
    var dropdown = document.getElementById("searchDropdown");
    if (!input || !dropdown) return;

    var timer = null;

    input.addEventListener("input", function () {
        clearTimeout(timer);
        var q = this.value.trim();

        if (q.length < 2) {
            close();
            return;
        }
        timer = setTimeout(function () { suggest(q); }, 280);
    });

    input.addEventListener("focus", function () {
        if (this.value.trim().length >= 2) {
            dropdown.classList.add("open");
        }
    });

    document.addEventListener("click", function (e) {
        if (!input.contains(e.target) && !dropdown.contains(e.target)) {
            close();
        }
    });

    input.addEventListener("keydown", function (e) {
        if (e.key === "Escape") { close(); input.blur(); }
    });

    function suggest(q) {
        dropdown.innerHTML =
            '<div class="search-dd-item text-muted" style="font-size:.8rem;">' +
                '<i class="fas fa-search"></i>' +
                ' Press Enter to search for "' + esc(q) + '"' +
            '</div>';
        dropdown.classList.add("open");
    }

    function close() {
        dropdown.classList.remove("open");
    }

    function esc(str) {
        return str.replace(/[&<>"']/g, function (c) {
            return { "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;" }[c];
        });
    }
}());


/* ============================================================
   8. SMOOTH REVEAL on scroll
============================================================ */
(function initReveal() {
    if (!window.IntersectionObserver) return;

    var style = document.createElement("style");
    style.textContent =
        ".reveal-on-scroll{opacity:0;transform:translateY(24px);transition:opacity .5s ease,transform .5s ease;}" +
        ".reveal-on-scroll.revealed{opacity:1;transform:translateY(0);}";
    document.head.appendChild(style);

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("revealed");
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.08, rootMargin: "0px 0px -40px 0px" });

    document.querySelectorAll(".reveal-on-scroll").forEach(function (el) {
        observer.observe(el);
    });
}());


/* ============================================================
   9. HERO CAROUSEL — animate content on slide change
============================================================ */
(function initHeroCarousel() {
    var carousel = document.getElementById("heroCarousel");
    if (!carousel) return;

    function animateIn(item) {
        var content = item.querySelector(".hero-content");
        if (!content) return;
        content.style.opacity   = "0";
        content.style.transform = "translateY(30px)";
        requestAnimationFrame(function () {
            content.style.transition = "opacity .7s ease, transform .7s ease";
            content.style.opacity    = "1";
            content.style.transform  = "translateY(0)";
        });
    }

    // Animate the first slide on load
    var activeItem = carousel.querySelector(".carousel-item.active");
    if (activeItem) setTimeout(function () { animateIn(activeItem); }, 200);

    // Animate on every slide change
    carousel.addEventListener("slid.bs.carousel", function (e) {
        animateIn(e.relatedTarget);
    });
}());


/* ============================================================
   10. NEWSLETTER FORM
============================================================ */
(function initNewsletter() {
    var form = document.getElementById("newsletterForm");
    if (!form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        var email = form.querySelector('input[type="email"]');
        if (email && email.value) {
            window.showToast("🎉 Thank you! You're now subscribed.", "success");
            form.reset();
        }
    });
}());


/* ============================================================
   11. QUANTITY STEPPER — generic +/- buttons
============================================================ */
document.addEventListener("click", function (e) {
    var btn = e.target.closest("[data-qty-btn]");
    if (!btn) return;

    var input = document.getElementById(btn.dataset.qtyBtn);
    if (!input) return;

    var min = parseInt(input.min || "1",   10);
    var max = parseInt(input.max || "999", 10);
    var val = parseInt(input.value || "1", 10);

    if (btn.dataset.dir === "up")   val = Math.min(val + 1, max);
    if (btn.dataset.dir === "down") val = Math.max(val - 1, min);

    input.value = val;
    input.dispatchEvent(new Event("change", { bubbles: true }));
});