Gunakan template ini untuk automation patrol yang harus mengerjakan kerja nyata per cycle.

---

Kerjakan [OBJECTIVE] dengan cycle ketat satu [UNIT_OF_WORK] per satu waktu.

Source of truth utama:
- [SOURCE_OF_TRUTH_1]
- [SOURCE_OF_TRUTH_2]

Aturan cycle:
1. Di awal setiap cycle, pilih tepat satu [UNIT_OF_WORK] yang masih unfinished.
2. Kerjakan hanya unit itu pada cycle ini. Jangan pecah fokus ke beberapa unit dalam cycle yang sama.
3. Ikuti workflow kerja fitur/item ini:
   1. [STEP_1]
   2. [STEP_2]
   3. [STEP_3]
   4. [STEP_4]
   5. [STEP_5]
4. Review hasil kerja unit tersebut sampai statusnya jelas: `completed` atau `blocked`.

Aturan blocked vs greenfield:
- Tandai `blocked` jika [BLOCKED_RULE].
- Tetap kerjakan sebagai scope baru jika [GREENFIELD_RULE].
- Jangan menganggap semua item tanpa existing sebagai blocked.

Aturan notifikasi:
- Setelah setiap cycle `completed` atau `blocked`, wajib kirim update status Telegram melalui skill local `telegram-bot-sender` memakai alias bot `[BOT_ALIAS]`.
- Pesan harus menyebut nama [UNIT_OF_WORK], status `completed` atau `blocked`, dan apa saja yang masih tersisa.
- Pengiriman Telegram adalah bagian dari completion cycle. Jangan berhenti setelah edit file atau update artefak.

Aturan bahasa:
- [LANGUAGE_RULE]

Aturan continuity:
- Lanjutkan di thread yang sama jika diminta atau jika `target_thread_id` sudah ditetapkan.
- Jangan sengaja membuat chat baru untuk setiap cycle.

Aturan selesai total:
- Kalau semua [UNIT_OF_WORK] yang required sudah selesai, kirim pesan Telegram final melalui `[BOT_ALIAS]` yang menyatakan bahwa semuanya sudah selesai.
- Setelah pesan final itu berhasil dikirim, anggap automation ini selesai dan jangan lanjut cycle baru lagi.

Larangan:
- Jangan ubah tugas kerja nyata menjadi heartbeat validation.
- Jangan kirim balasan no-op seperti `Instruksi automation masih relevan`.
- Jangan anggap cycle selesai jika Telegram belum terkirim.
