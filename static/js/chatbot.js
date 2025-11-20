// static/js/chatbot.js
(function () {
  // Debug prefix
  const DBG = '[Chatbot]';

  // Utility to safe-log
  function safeLog(...args) {
    if (window.console && console.log) console.log(DBG, ...args);
  }

  // DOM-ready helper
  function onReady(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function getToggle() {
    return document.getElementById('style-assistant-btn');
  }

  function getPopup() {
    return document.getElementById('style-assistant-popup');
  }

  // Open/close functions must be globally callable for inline fallback
  window.openStyleAssistant = function openStyleAssistant() {
    safeLog('openStyleAssistant called');
    const popup = getPopup();
    if (!popup) {
      safeLog('ERROR: popup element not found');
      return;
    }
    popup.classList.add('sa-open');
    popup.setAttribute('aria-hidden', 'false');
    document.body.classList.add('sa-popup-active', 'sa-backdrop-visible');
    // focus first button for accessibility
    const firstBtn = popup.querySelector('.sa-action-btn');
    if (firstBtn) setTimeout(() => firstBtn.focus(), 80);
  };

  window.closeStyleAssistant = function closeStyleAssistant() {
    safeLog('closeStyleAssistant called');
    const popup = getPopup();
    if (!popup) return;
    popup.classList.remove('sa-open');
    popup.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('sa-popup-active', 'sa-backdrop-visible');
    // return focus to toggle button
    const toggle = getToggle();
    if (toggle) toggle.focus();
  };

  onReady(function () {
    safeLog('chatbot.js loaded');

    const toggle = getToggle();
    let popup = getPopup();

    if (!toggle) {
      safeLog('ERROR: style-assistant-btn not found in DOM');
      return;
    }
    if (!popup) {
      safeLog('ERROR: style-assistant-popup not found in DOM');
      // create a minimal popup fallback so click won't be silent
      const fb = document.createElement('div');
      fb.id = 'style-assistant-popup';
      fb.className = 'sa-popup';
      fb.setAttribute('aria-hidden', 'true');
      fb.innerHTML = '<div class="sa-popup-inner"><button onclick="closeStyleAssistant()">Close</button><div class="sa-msg">Profile missing or popup not found</div></div>';
      document.body.appendChild(fb);
    }

    // Attach event listeners robustly
    function handleToggle(e) {
      safeLog('toggle clicked or activated', e.type);
      popup = getPopup();
      if (!popup) {
        safeLog('Popup missing at toggle time');
        return;
      }
      // If popup open -> close; else open
      const isOpen = popup && popup.classList.contains('sa-open');
      if (isOpen) window.closeStyleAssistant();
      else window.openStyleAssistant();
    }

    // Click listener
    toggle.addEventListener('click', handleToggle, false);

    // Keyboard activation (Enter/Space)
    toggle.addEventListener('keydown', function (ev) {
      if (ev.key === 'Enter' || ev.key === ' ') {
        ev.preventDefault();
        handleToggle(ev);
      }
    }, false);

    safeLog('Event listeners attached');

    // Attach action buttons inside popup
    function attachActionHandlers() {
      const actionButtons = document.querySelectorAll('.sa-action-btn');
      actionButtons.forEach(btn => {
        if (btn.dataset.listenerAttached === 'true') {
          return;
        }
        btn.dataset.listenerAttached = 'true';
        btn.addEventListener('click', async function (ev) {
          const key = btn.dataset.key;
          safeLog('Action clicked:', key);
          // show loading
          const out = document.getElementById('sa-output');
          if (out) out.innerHTML = '<div class="sa-loading">Loading suggestions...</div>';

          // Fetch user profile
          let profile = null;
          try {
            // Try root-level endpoint first, fallback to accounts path
            let resp = await fetch('/profile/data/', { credentials: 'same-origin' });
            if (!resp.ok) {
              safeLog('Root endpoint failed, trying accounts path');
              resp = await fetch('/accounts/profile/data/', { credentials: 'same-origin' });
            }
            if (resp.ok) {
              const data = await resp.json();
              // Handle both old format (exists) and new format (profile)
              if (data.profile) {
                profile = data;
              } else if (data.exists) {
                // Convert old format to new format
                profile = {
                  profile: {
                    height: data.height,
                    skin_tone: data.skin_tone,
                    body_type: data.body_type,
                    favourite_colors: data.favourite_colors || [],
                    preferred_clothing_types: data.preferred_clothing_types || []
                  }
                };
              }
            } else {
              safeLog('Profile endpoint returned non-ok:', resp.status);
            }
          } catch (err) {
            safeLog('Error fetching profile:', err);
          }

          // If no profile, show message
          if (!profile || !profile.profile) {
            if (out) out.innerHTML = '<div class="sa-error">Please complete your style profile to get personalised suggestions.</div>';
            return;
          }

          // Generate answer locally using rules. (Simple switch)
          const answer = generateAnswer(key, profile.profile);
          if (out) out.innerHTML = `<div class="sa-answer"><strong>${btn.innerText}</strong><p>${answer}</p></div>`;
        });
      });
      safeLog('Action handlers attached:', actionButtons.length);
    }

    // simple rule-based answer generator - expand as needed
    function generateAnswer(key, profile) {
      const skin = (profile.skin_tone || '').toLowerCase();
      const body = (profile.body_type || '').toLowerCase();
      const favs = profile.favourite_colors || [];

      // Basic rules
      const colorMap = {
        'fair/light': ['pastel blue', 'navy', 'maroon', 'olive'],
        'wheatish': ['teal', 'brown', 'white', 'mustard'],
        'dark': ['bright red', 'royal blue', 'gold', 'yellow']
      };
      const bodyMap = {
        'slim': 'Layered outfits, oversized tees and structured jackets work well for you.',
        'fit': 'Slim-fit shirts, well-tailored chinos, and polo tees will highlight your build.',
        'fat': 'Choose vertical patterns, darker shades and relaxed fits to balance proportions.'
      };
      if (key === 'colors') {
        const base = colorMap[skin] || ['neutral tones like white, black, navy'];
        const priority = (favs.length ? favs.join(', ') + ' (your favourites) — try combining with ' + base.slice(0,3).join(', ') : base.join(', '));
        return `Based on your skin tone (${skin || 'unknown'}) and favourite colors (${favs.join(', ') || 'none'}): ${priority}.`;
      } else if (key === 'body') {
        return bodyMap[body] || 'Use balanced proportions, avoid overly tight clothes and choose clothes that fit well.';
      } else if (key === 'trending') {
        return 'Trending styles now: oversized tees, cargo pants, denim jackets, neutral-layered looks and white sneakers.';
      } else if (key === 'combinations') {
        // basic combos based on first favourite color
        const fav = favs[0] || 'blue';
        const combos = {
          'black': 'Black + White, Black + Olive, Black + Beige',
          'blue': 'Blue + Beige, Blue + White, Blue + Grey',
          'red': 'Red + Black, Red + Navy',
          'green': 'Green + Brown, Green + Beige'
        };
        return combos[fav.toLowerCase()] || `Good combos: ${fav} + White, ${fav} + Beige, Neutral accents.`;
      } else if (key === 'favourite') {
        return `Outfits using your favourite colors (${favs.join(', ') || 'none'}): try pairing one favourite color as a statement piece with neutral bottoms and matching accessories.`;
      }
      return 'Try filling your profile for better suggestions.';
    }

    // Attach handlers now (in case popup already in DOM)
    attachActionHandlers();

    // Also re-run attach handlers when popup content is changed or injected
    const observerTarget = getPopup() || document.body;
    const observer = new MutationObserver(() => attachActionHandlers());
    observer.observe(observerTarget, { childList: true, subtree: true });

    // Close when clicking outside popup
    document.addEventListener('click', (event) => {
      const popupEl = getPopup();
      const toggleEl = getToggle();
      if (!popupEl) return;
      const clickedToggle = toggleEl && (toggleEl === event.target || toggleEl.contains(event.target));
      const insidePopup = popupEl.contains(event.target);
      if (!clickedToggle && !insidePopup && popupEl.classList.contains('sa-open')) {
        safeLog('Closing because of outside click');
        window.closeStyleAssistant();
      }
    });

    // final debug badge
    if (window.DEBUG) {
      const badge = document.createElement('div');
      badge.style.position = 'fixed';
      badge.style.right = '10px';
      badge.style.bottom = '110px';
      badge.style.padding = '6px 8px';
      badge.style.background = '#1f2937';
      badge.style.color = 'white';
      badge.style.borderRadius = '6px';
      badge.style.zIndex = 999999;
      badge.innerText = 'Chatbot JS OK';
      document.body.appendChild(badge);
    }
  });

})();
