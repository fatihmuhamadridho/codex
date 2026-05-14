# Automation Debug Checklist

Gunakan checklist ini saat automation patrol tidak berperilaku seperti yang diinginkan.

## A. Automation ada tapi tidak eksekusi kerja

- Pastikan `kind = "cron"` jika tujuan automation adalah kerja nyata terjadwal.
- Pastikan `status = "ACTIVE"`.
- Pastikan `rrule` memakai format `RRULE:...`.
- Pastikan `cwds` menunjuk ke workspace yang benar.
- Baca prompt-nya. Jika prompt lebih mirip health check daripada instruksi kerja, perbaiki prompt.

## B. Automation hilang dari UI

- Pastikan file `automation.toml` masih ada.
- Pastikan TOML valid dan tidak ada field penting yang hilang.
- Cek field loader-sensitive:
  - `version`
  - `id`
  - `name`
  - `kind`
  - `status`
  - `rrule`
  - `model`
  - `reasoning_effort`
  - `execution_environment`
  - `cwds`

## C. Automation berubah jadi heartbeat/no-op

- Ganti `kind` dari `heartbeat` ke `cron` bila ini memang automation kerja nyata.
- Hapus prompt yang hanya mengembalikan status seperti `Instruksi automation masih relevan`.
- Tambahkan unit kerja eksplisit per cycle dan condition selesai.

## D. Automation pecah ke banyak thread

- Set `target_thread_id` bila user meminta single-thread continuity.
- Tulis juga di prompt bahwa automation harus lanjut di thread yang sama.
- Ingat: prompt membantu, tetapi `target_thread_id` biasanya lebih menentukan dibanding wording prompt saja.

## E. Telegram tidak terkirim

- Pastikan alias bot benar.
- Pastikan prompt menyebut Telegram sebagai bagian wajib dari completion cycle.
- Pastikan isi pesan jelas: nama item, status, sisa pekerjaan.

## F. Memory drift

- Baca `$CODEX_HOME/automations/<automation_id>/memory.md`.
- Pastikan memory mencatat perubahan penting terakhir.
- Jangan biarkan prompt baru bertentangan dengan aturan yang disimpan di memory tanpa alasan jelas.
