#!/usr/bin/env node

const WebSocket = require("ws");

const port = process.env.CDP_PORT || process.argv[2] || "9223";
const command = process.argv[3];
const argText = process.argv.slice(4).join(" ");

if (!command) {
  console.error("usage: teams_session.js <port> <command> [text]");
  process.exit(1);
}

async function fetchJson(path) {
  const response = await fetch(`http://127.0.0.1:${port}${path}`);
  if (!response.ok) {
    throw new Error(`failed request ${path}: ${response.status}`);
  }
  return response.json();
}

function isTeamsTarget(target) {
  const title = target.title || "";
  const url = target.url || "";
  return /Microsoft Teams|teams/i.test(title) ||
    /teams\.cloud\.microsoft|teams\.microsoft\.com/i.test(url);
}

function tailText(text, size = 1400) {
  if (!text) return "";
  return text.slice(Math.max(0, text.length - size));
}

async function getTeamsTarget() {
  const targets = await fetchJson("/json/list");
  const pages = targets.filter((target) => target.type === "page");
  const match = pages.find(isTeamsTarget);
  if (!match) {
    throw new Error("no Teams page target found");
  }
  return match;
}

async function withTarget(fn) {
  const target = await getTeamsTarget();
  const ws = new WebSocket(target.webSocketDebuggerUrl);
  let nextId = 0;
  const pending = new Map();

  const send = (method, params = {}) =>
    new Promise((resolve, reject) => {
      const id = ++nextId;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params }));
    });

  ws.on("message", (chunk) => {
    const message = JSON.parse(chunk);
    if (message.id && pending.has(message.id)) {
      const ticket = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) {
        ticket.reject(new Error(message.error.message));
      } else {
        ticket.resolve(message.result);
      }
    }
  });

  await new Promise((resolve) => ws.once("open", resolve));
  await send("Runtime.enable");
  await send("Page.enable");

  try {
    return await fn({ target, send });
  } finally {
    ws.close();
  }
}

async function evaluate(send, expression) {
  const result = await send("Runtime.evaluate", {
    expression,
    returnByValue: true,
  });
  return result.result.value;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function esc(send) {
  return Promise.all([
    send("Input.dispatchKeyEvent", {
      type: "keyDown",
      windowsVirtualKeyCode: 27,
      code: "Escape",
      key: "Escape",
      nativeVirtualKeyCode: 27,
    }),
    send("Input.dispatchKeyEvent", {
      type: "keyUp",
      windowsVirtualKeyCode: 27,
      code: "Escape",
      key: "Escape",
      nativeVirtualKeyCode: 27,
    }),
  ]);
}

async function openSearch(send) {
  return evaluate(send, `(() => {
    const btn = [...document.querySelectorAll('button,[role="button"]')]
      .find((node) => (node.getAttribute('aria-label') || '').includes('Expand search box'));
    if (!btn) return { ok: false, reason: 'no search button' };
    btn.click();
    return { ok: true };
  })()`);
}

async function focusSearchInput(send) {
  return evaluate(send, `(() => {
    const input = [...document.querySelectorAll('input,textarea,[contenteditable="true"]')]
      .find((node) => {
        const placeholder = node.placeholder || '';
        const aria = node.getAttribute('aria-label') || '';
        return placeholder.includes('Search')
          || placeholder.includes('Look for people, messages, files, and more')
          || aria.includes('Search')
          || aria.includes('Look for people, messages, files, and more');
      });
    if (!input) return { ok: false, reason: 'no search input' };
    input.focus();
    return {
      ok: true,
      tag: input.tagName,
      isContentEditable: !!input.isContentEditable,
      placeholder: input.getAttribute('placeholder') || '',
      value: input.isContentEditable ? input.innerText : input.value
    };
  })()`);
}

async function clearSearch(send) {
  const cleared = await evaluate(send, `(() => {
    const input = [...document.querySelectorAll('input,textarea,[contenteditable="true"]')]
      .find((node) => {
        const placeholder = node.placeholder || '';
        const aria = node.getAttribute('aria-label') || '';
        return placeholder.includes('Search')
          || placeholder.includes('Look for people, messages, files, and more')
          || aria.includes('Search')
          || aria.includes('Look for people, messages, files, and more');
      });
    if (!input) return { ok: false, reason: 'no search input' };
    input.focus();
    if (input.isContentEditable) {
      input.innerText = '';
      input.dispatchEvent(new InputEvent('input', { bubbles: true, inputType: 'deleteContentBackward', data: null }));
      return { ok: true, value: input.innerText };
    }
    input.value = '';
    input.dispatchEvent(new Event('input', { bubbles: true }));
    input.dispatchEvent(new Event('change', { bubbles: true }));
    return { ok: true, value: input.value };
  })()`);
  if (!cleared.ok) {
    return cleared;
  }
  await sleep(250);
  return focusSearchInput(send);
}

async function searchState(send) {
  return evaluate(send, `(() => ({
    title: document.title,
    text: document.body ? document.body.innerText : ''
  }))()`);
}

async function searchQuery(send, text) {
  await openSearch(send);
  await sleep(300);
  const cleared = await clearSearch(send);
  if (!cleared.ok) {
    return { ok: false, stage: "clear", cleared };
  }
  await send("Input.insertText", { text });
  await sleep(1600);
  const state = await searchState(send);
  return {
    ok: true,
    query: text,
    state,
  };
}

async function openResult(send, text) {
  const escaped = JSON.stringify(text);
  return evaluate(send, `(() => {
    function visible(el) {
      return !!(el && (el.offsetWidth || el.offsetHeight || el.getClientRects().length));
    }
    const nodes = [...document.querySelectorAll('*')];
    const exactMatches = nodes.filter((node) => visible(node) && (node.innerText || '').trim() === ${escaped});
    const containsMatches = nodes.filter((node) => visible(node) && (node.innerText || '').includes(${escaped}));
    const exact = exactMatches.sort((a, b) => (a.innerText || '').length - (b.innerText || '').length)[0];
    const contains = containsMatches.sort((a, b) => (a.innerText || '').length - (b.innerText || '').length)[0];
    const pick = exact || contains;
    if (!pick) return { ok: false, reason: 'no matching result' };
    pick.scrollIntoView({ block: 'center' });
    pick.dispatchEvent(new MouseEvent('mousedown', { bubbles: true, cancelable: true, view: window }));
    pick.dispatchEvent(new MouseEvent('mouseup', { bubbles: true, cancelable: true, view: window }));
    pick.dispatchEvent(new MouseEvent('click', { bubbles: true, cancelable: true, view: window }));
    return {
      ok: true,
      text: (pick.innerText || '').trim().slice(0, 200)
    };
  })()`);
}

async function openDm(send, text) {
  const searched = await searchQuery(send, text);
  if (!searched.ok) {
    return searched;
  }
  let opened = await openResult(send, text);
  await sleep(1800);
  let state = await searchState(send);
  if ((state.title || "").includes("Search")) {
    opened = await openResult(send, text);
    await sleep(1800);
    state = await searchState(send);
  }
  return {
    ok: opened.ok && (state.title.includes(text) || state.text.includes(text)),
    searched,
    opened,
    state,
  };
}

async function focusComposer(send) {
  return evaluate(send, `(() => {
    const el = [...document.querySelectorAll('[contenteditable="true"]')]
      .find((node) => (node.getAttribute('aria-label') || '') === 'Type a message');
    if (!el) return { ok: false, reason: 'no composer' };
    el.scrollIntoView({ block: 'center' });
    el.focus();
    return {
      ok: true,
      active: document.activeElement === el,
      html: el.innerHTML,
      text: el.innerText
    };
  })()`);
}

async function composerState(send) {
  return evaluate(send, `(() => {
    const el = [...document.querySelectorAll('[contenteditable="true"]')]
      .find((node) => (node.getAttribute('aria-label') || '') === 'Type a message');
    if (!el) return { ok: false, reason: 'no composer' };
    return {
      ok: true,
      active: document.activeElement === el,
      html: el.innerHTML,
      text: el.innerText
    };
  })()`);
}

async function insertMessage(send, text) {
  await focusComposer(send);
  await send("Input.insertText", { text });
  return composerState(send);
}

async function clickSend(send) {
  return evaluate(send, `(() => {
    const btn = [...document.querySelectorAll('button,[role="button"]')]
      .find((node) => (node.getAttribute('aria-label') || '').startsWith('Send'));
    if (!btn) return { ok: false, reason: 'no send button' };
    btn.click();
    return { ok: true, aria: btn.getAttribute('aria-label') };
  })()`);
}

async function pageState(send, target) {
  const value = await evaluate(send, `(() => ({
    href: location.href,
    title: document.title,
    text: document.body ? document.body.innerText : ''
  }))()`);
  return {
    targetId: target.id,
    title: value.title,
    href: value.href,
    tail: tailText(value.text),
  };
}

async function main() {
  if (command === "state") {
    const output = await withTarget(async ({ target, send }) => pageState(send, target));
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "tail") {
    const output = await withTarget(async ({ send }) => {
      const state = await evaluate(send, "document.body ? document.body.innerText : ''");
      return { tail: tailText(state, 2500) };
    });
    console.log(output.tail);
    return;
  }

  if (command === "open-search") {
    const output = await withTarget(async ({ send }) => openSearch(send));
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "clear-search") {
    const output = await withTarget(async ({ send }) => {
      await openSearch(send);
      return clearSearch(send);
    });
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "search-state") {
    const output = await withTarget(async ({ send }) => searchState(send));
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "search-query") {
    if (!argText) {
      throw new Error("search-query requires text");
    }
    const output = await withTarget(async ({ send }) => searchQuery(send, argText));
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "open-result") {
    if (!argText) {
      throw new Error("open-result requires text");
    }
    const output = await withTarget(async ({ send }) => {
      const opened = await openResult(send, argText);
      await sleep(1800);
      const state = await searchState(send);
      return { opened, state };
    });
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "open-dm") {
    if (!argText) {
      throw new Error("open-dm requires text");
    }
    const output = await withTarget(async ({ send }) => openDm(send, argText));
    console.log(JSON.stringify(output, null, 2));
    process.exit(output.ok ? 0 : 2);
    return;
  }

  if (command === "close-search-overlay") {
    const output = await withTarget(async ({ send }) => {
      await esc(send);
      const state = await composerState(send);
      return { closed: true, composer: state };
    });
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "focus-composer") {
    const output = await withTarget(async ({ send }) => focusComposer(send));
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "type-message") {
    if (!argText) {
      throw new Error("type-message requires text");
    }
    const output = await withTarget(async ({ send }) => {
      await esc(send);
      return insertMessage(send, argText);
    });
    console.log(JSON.stringify(output, null, 2));
    return;
  }

  if (command === "send-message") {
    if (!argText) {
      throw new Error("send-message requires text");
    }
    const output = await withTarget(async ({ target, send }) => {
      await esc(send);
      const before = await insertMessage(send, argText);
      if (!before.ok || !String(before.text || "").includes(argText)) {
        return { ok: false, stage: "type", before };
      }

      await new Promise((resolve) => setTimeout(resolve, 1800));
      const sendResult = await clickSend(send);
      await new Promise((resolve) => setTimeout(resolve, 1800));
      const after = await pageState(send, target);
      return {
        ok: after.tail.includes(argText),
        stage: "verify",
        before,
        sendResult,
        after,
      };
    });
    console.log(JSON.stringify(output, null, 2));
    process.exit(output.ok ? 0 : 2);
    return;
  }

  throw new Error(`unknown command: ${command}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
