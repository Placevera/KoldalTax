// Sends contact and newsletter forms to the Supabase "contact" edge function.
(function () {
  const cfg = window.KT_CONFIG || {};
  const endpoint = cfg.SUPABASE_URL + "/functions/v1/contact";
  document.querySelectorAll("form[data-kind]").forEach((form) => {
    const msg = form.querySelector(".msg");
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const btn = form.querySelector("button[type=submit]");
      const data = Object.fromEntries(new FormData(form));
      data.kind = form.dataset.kind;
      // Fold extra questions (fields named x_*) into the message so the email shows them.
      const extras = [...form.querySelectorAll("[name^=x_]")].filter((el) => el.value).map((el) => el.closest("label").firstChild.textContent.replace(/\s*\(.*\)\s*$/, "").trim() + ": " + el.value.trim());
      Object.keys(data).filter((k) => k.startsWith("x_")).forEach((k) => delete data[k]);
      if (extras.length) data.message = extras.join("\n") + (data.message ? "\n\n" + data.message : "");
      data.page = location.pathname;
      btn.disabled = true;
      msg.className = "msg";
      try {
        const res = await fetch(endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json", apikey: cfg.SUPABASE_ANON_KEY, Authorization: "Bearer " + cfg.SUPABASE_ANON_KEY },
          body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error(await res.text());
        form.reset();
        msg.textContent = form.dataset.kind === "newsletter" ? "Thanks, you're on the list." : "Thanks! Your message was sent. I'll get back to you soon.";
        msg.className = "msg ok";
      } catch (err) {
        msg.textContent = "Sorry, something went wrong. Please email alek@koldaltax.com directly.";
        msg.className = "msg err";
      } finally {
        btn.disabled = false;
      }
    });
  });
})();
