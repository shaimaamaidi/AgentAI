const form = document.getElementById('urlForm');
const input = document.getElementById('urlInput');
const messages = document.getElementById('messages');
const chatContainer = document.getElementById('chat');
const status = document.getElementById('status');

function escapeHtml(str) {
  return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function addMessage(role, text, id) {
  const wrapper = document.createElement('div');
  wrapper.className = 'message ' + role;
  if (id) wrapper.id = id;
  wrapper.dataset.buffer = text || '';
  
  renderBufferToElement(wrapper);
  messages.appendChild(wrapper);
  scrollToBottom();
  return wrapper;
}

function renderBufferToElement(el) {
  const buf = el.dataset.buffer || '';
  let out = '';
  let i = 0;
  while (i < buf.length) {
    const start = buf.indexOf('```', i);
    if (start === -1) {
      out += '<div>' + escapeHtml(buf.slice(i)) + '</div>';
      break;
    }

    if (start > i) out += '<div>' + escapeHtml(buf.slice(i, start)) + '</div>';

    const after = buf.slice(start + 3);
    const end = after.indexOf('```');
    let codeContent = '';
    if (end === -1) {
      codeContent = after; 
      i = buf.length;
    } else {
      codeContent = after.slice(0, end);
      i = start + 3 + end + 3;
    }

    const firstLineMatch = codeContent.match(/^([a-zA-Z0-9_-]+)\r?\n/);
    if (firstLineMatch) {
      codeContent = codeContent.slice(firstLineMatch[0].length);
    }

    out += '<div class="code-block"><pre class="code">' + escapeHtml(codeContent) + '</pre></div>';
  }

  el.innerHTML = out;
  scrollToBottom();
}
function scrollToBottom(forceInstant = false) {
  try {
    requestAnimationFrame(() => {
      if (!chatContainer) return;
      const behavior = forceInstant ? 'auto' : 'smooth';
      chatContainer.scrollTo({ top: chatContainer.scrollHeight, behavior });
    });
  } catch (e) {
    if (chatContainer) chatContainer.scrollTop = chatContainer.scrollHeight;
  }
}

function isGitUrl(u) {
  if (!u || typeof u !== 'string') return false;
  const s = u.trim();
  if (!s) return false;
  if (/github\.com|gitlab\.com|bitbucket\.org/i.test(s)) return true;
  if (/\.git(\/)?$/i.test(s)) return true;
  if (/^https?:\/\/.+\.git$/i.test(s)) return true;
  return false;
}

form.addEventListener('submit', async (e) => {
  e.preventDefault();
  messages.innerHTML = '';
  status.textContent = '';

  const url = input.value.trim();
  if (!isGitUrl(url)) {
    status.textContent = "Désolé, tu dois donner un URL git valide.";
    addMessage('system', "Désolé, tu dois donner un URL git valide.");
    return;
  }

  addMessage('user', url);
  input.value = '';
  input.focus();

  try {
    status.textContent = 'Connexion au serveur...';
    const endpoint = `/generate-tests?url_repo=${encodeURIComponent(url)}`;
    const res = await fetch(endpoint);
    if (!res.ok) {
      const txt = await res.text();
      status.textContent = `Erreur: ${res.status} ${txt}`;
      addMessage('system', `Erreur: ${res.status} ${txt}`);
      return;
    }

    status.textContent = 'Streaming en cours...';
    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    const botId = 'bot-' + Date.now();
    const botEl = addMessage('bot', '', botId);

    let done = false;
    while (!done) {
      const { value, done: d } = await reader.read();
      done = d;
      if (value) {
        const chunk = decoder.decode(value, { stream: true });
        botEl.dataset.buffer = (botEl.dataset.buffer || '') + chunk;
        renderBufferToElement(botEl);
        scrollToBottom(true);
      }
    }

    status.textContent = 'Terminé.';
  } catch (err) {
    status.textContent = 'Erreur réseau: ' + err.message;
    addMessage('system', 'Erreur réseau: ' + err.message);
  }
});
