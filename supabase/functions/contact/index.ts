// Receives contact and newsletter forms from koldaltax.com, saves them, and emails Alek.
// Secrets (set with `supabase secrets set`): RESEND_API_KEY, NOTIFY_EMAIL, FROM_EMAIL.
import { createClient } from "npm:@supabase/supabase-js@2";

const ALLOWED_ORIGINS = ["https://www.koldaltax.com", "https://koldaltax.com"];

const cors = (origin: string | null) => ({
  "Access-Control-Allow-Origin": origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
  "Access-Control-Allow-Headers": "authorization, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
});

const clean = (v: unknown, max = 2000) => (typeof v === "string" ? v.trim().slice(0, max) : "");
const escape = (s: string) => s.replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]!));

Deno.serve(async (req) => {
  const headers = cors(req.headers.get("origin"));
  if (req.method === "OPTIONS") return new Response("ok", { headers });
  if (req.method !== "POST") return new Response("Method not allowed", { status: 405, headers });

  let body: Record<string, unknown>;
  try {
    body = await req.json();
  } catch {
    return new Response("Bad request", { status: 400, headers });
  }

  // Honeypot: bots fill the hidden "website" field. Pretend success.
  if (clean(body.website)) return new Response("ok", { headers });

  const kind = body.kind === "newsletter" ? "newsletter" : "contact";
  const row = {
    kind,
    first_name: clean(body.first_name, 100),
    last_name: clean(body.last_name, 100),
    email: clean(body.email, 200),
    phone: clean(body.phone, 50),
    service: clean(body.service, 100),
    message: clean(body.message, 5000),
    page: clean(body.page, 200),
  };
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(row.email)) return new Response("Invalid email", { status: 400, headers });
  if (kind === "contact" && !row.message) return new Response("Message required", { status: 400, headers });

  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
  const { data, error } = await db.from("submissions").insert(row).select("id").single();
  if (error) {
    console.error(error);
    return new Response("Could not save", { status: 500, headers });
  }

  const name = `${row.first_name} ${row.last_name}`.trim() || row.email;
  const subject = kind === "contact" ? `New inquiry from ${name}: ${row.service || "Website"}` : `New newsletter signup: ${row.email}`;
  const lines = kind === "contact"
    ? [["Name", name], ["Email", row.email], ["Phone", row.phone || "-"], ["Service", row.service || "-"], ["Message", row.message]]
    : [["Email", row.email], ["Signed up on", row.page]];
  const html = lines.map(([k, v]) => `<p><strong>${k}:</strong><br>${escape(v).replace(/\n/g, "<br>")}</p>`).join("");

  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: { Authorization: `Bearer ${Deno.env.get("RESEND_API_KEY")}`, "Content-Type": "application/json" },
    body: JSON.stringify({
      from: Deno.env.get("FROM_EMAIL") ?? "Koldal Tax Website <website@koldaltax.com>",
      to: [Deno.env.get("NOTIFY_EMAIL") ?? "alek@koldaltax.com"],
      reply_to: row.email,
      subject,
      html,
    }),
  });
  if (res.ok) {
    await db.from("submissions").update({ emailed: true }).eq("id", data.id);
  } else {
    // The message is still saved in the table; log the failure so it can be checked.
    console.error("Resend failed", res.status, await res.text());
  }

  return new Response("ok", { headers });
});
