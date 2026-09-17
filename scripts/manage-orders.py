"""Local-only order editor. Run on the owner's desktop, never on public hosting."""
import copy
import importlib.util
import json
import shutil
import tkinter as tk
import uuid
from datetime import date
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'content/site.json'
spec = importlib.util.spec_from_file_location('compiler', ROOT / 'scripts/prepare-content.py')
compiler = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compiler)

# QR codes are generated only by the website configuration editor.
# The order manager does not require QR dependencies when saving orders.
# Prevent compile_site() from requesting qrcode during order updates.
def _skip_qr_generation(value, filename):
    return ''

compiler.create_qr = _skip_qr_generation

STATUSES = {'Proses pengerjaan': 'production', 'Proses pengiriman': 'shipping', 'Pesanan diterima': 'delivered'}


class Editor:
    def __init__(self, window):
        self.window = window
        self.source_bytes = SOURCE.read_bytes()
        self.data = json.loads(self.source_bytes)
        self.current = None
        self.photos = []
        window.title('GDT WORKS — Pengelola Pesanan Lokal')
        window.geometry('880x760')
        window.protocol('WM_DELETE_WINDOW', self.close)
        panel = ttk.Frame(window, padding=20)
        panel.pack(fill='both', expand=True)
        ttk.Label(panel, text='PENGELOLA PESANAN', font=('', 18, 'bold')).pack(anchor='w')
        ttk.Label(panel, text='Simpan memperbarui berkas lokal. Unggah ulang dist untuk memperbarui situs online.').pack(anchor='w', pady=8)
        self.orders = ttk.Combobox(panel, state='readonly')
        self.orders.pack(fill='x')
        self.orders.bind('<<ComboboxSelected>>', lambda _: self.load(self.orders.current()))
        order_actions = ttk.Frame(panel)
        order_actions.pack(fill='x', pady=8)
        ttk.Button(order_actions, text='+ Pesanan baru', command=self.new).pack(side='left')
        self.delete_button = ttk.Button(order_actions, text='Hapus pesanan', command=self.delete, state='disabled')
        self.delete_button.pack(side='left', padx=8)
        self.fields = {}
        for key, label in [('title', 'Nama pesanan / judul publik'), ('projectCode', 'Kode pesanan anonim'), ('stage', 'Detail tahap (mis. pengecatan / diserahkan ke kurir)'), ('description', 'Keterangan publik')]:
            ttk.Label(panel, text=label).pack(anchor='w')
            self.fields[key] = tk.StringVar()
            ttk.Entry(panel, textvariable=self.fields[key]).pack(fill='x', pady=(2, 7))
        ttk.Label(panel, text='Persentase pengerjaan (0–100)').pack(anchor='w')
        self.percentage = tk.IntVar(value=0)
        tk.Scale(panel, from_=0, to=100, orient='horizontal', variable=self.percentage).pack(fill='x')
        self.status = tk.StringVar(value='Proses pengerjaan')
        ttk.Combobox(panel, state='readonly', textvariable=self.status, values=list(STATUSES)).pack(fill='x', pady=6)
        ttk.Label(panel, text='Foto slide: 4–8 foto. Format: PNG, JPG, JPEG, WEBP. Nama file foto bebas tanpa batas karakter. Urutan daftar = urutan slide. Hapus lalu pilih untuk mengganti.').pack(anchor='w')
        self.photo_list = tk.Listbox(panel, height=5)
        self.photo_list.pack(fill='both', expand=True, pady=6)
        actions = ttk.Frame(panel)
        actions.pack(fill='x')
        ttk.Button(actions, text='Pilih foto…', command=self.choose_photos).pack(side='left')
        ttk.Button(actions, text='Hapus foto pilihan', command=self.remove_photo).pack(side='left', padx=8)
        self.approved = tk.BooleanVar(value=False)
        ttk.Checkbutton(panel, variable=self.approved, text='Setujui untuk publikasi (nama, foto, dan keterangan sudah mendapat izin)').pack(anchor='w', pady=12)
        ttk.Button(panel, text='Simpan pesanan & perbarui situs lokal', command=self.save).pack(fill='x')
        self.refresh()
        self.new()

    def refresh(self):
        self.orders['values'] = [entry['title'] for entry in self.data.get('progress', [])]

    def load(self, index):
        if not messagebox.askyesno('Buka pesanan', 'Perubahan formulir yang belum disimpan akan diabaikan. Lanjutkan?'):
            if self.current is None:
                self.orders.set('Pesanan baru — belum disimpan')
            else:
                self.orders.current(self.current)
            return
        self.delete_button.state(['!disabled'])
        self.current = index
        entry = self.data['progress'][index]
        for key, value in self.fields.items():
            value.set(entry.get(key, ''))
        self.percentage.set(entry.get('percentage', 0))
        self.status.set(next((label for label, code in STATUSES.items() if code == entry.get('status')), 'Proses pengerjaan'))
        self.approved.set(entry.get('approved') is True)
        self.photos = [(ROOT / 'dist' / photo['image'], photo['alt']) for photo in entry.get('photos', [])]
        self.refresh_photos()

    def new(self, confirm=True):
        if confirm and self.fields['title'].get() and not messagebox.askyesno('Pesanan baru', 'Abaikan perubahan formulir yang belum disimpan?'):
            return
        self.current = None
        self.delete_button.state(['disabled'])
        self.orders.set('Pesanan baru — belum disimpan')
        for value in self.fields.values():
            value.set('')
        self.percentage.set(0)
        self.status.set('Proses pengerjaan')
        self.approved.set(False)
        self.photos = []
        self.refresh_photos()

    def refresh_photos(self):
        self.photo_list.delete(0, 'end')
        for index, (path, _) in enumerate(self.photos):
            self.photo_list.insert('end', f'{index + 1}. {path.name}')

    def choose_photos(self):
        files = filedialog.askopenfilenames(filetypes=[('Foto', '*.jpg *.jpeg *.png *.webp')])
        if len(self.photos) + len(files) > 8:
            messagebox.showerror('Foto', 'Maksimal 8 foto per pesanan.')
            return
        self.photos.extend((Path(path), '') for path in files)
        self.refresh_photos()

    def remove_photo(self):
        selected = self.photo_list.curselection()
        if selected:
            self.photos.pop(selected[0])
            self.refresh_photos()

    def save(self):
        try:
            if SOURCE.read_bytes() != self.source_bytes:
                raise ValueError('Data diubah di luar panel. Tutup dan buka ulang panel agar perubahan tidak tertimpa.')
            entry = copy.deepcopy(self.data['progress'][self.current]) if self.current is not None else {'id': 'order-' + uuid.uuid4().hex[:12], 'timeline': []}
            for key, value in self.fields.items():
                entry[key] = compiler.text(value.get(), key)
            if not 4 <= len(self.photos) <= 8:
                raise ValueError('Pilih minimal 4 dan maksimal 8 foto.')
            percent = self.percentage.get()
            status = STATUSES[self.status.get()]
            if status != 'production' and percent != 100:
                raise ValueError('Atur pengerjaan ke 100% sebelum memilih pengiriman atau diterima.')
            entry.update(percentage=percent, status=status, approved=self.approved.get(), date=date.today().isoformat(), photos=[])
            for index, (path, alt) in enumerate(self.photos):
                if not path.is_file() or path.suffix.lower() not in ['.jpg', '.jpeg', '.png', '.webp']:
                    raise ValueError('Foto tidak tersedia atau format tidak didukung: ' + path.name)
                try:
                    relative = path.resolve().relative_to((ROOT / 'dist/assets').resolve())
                    destination = ROOT / 'dist/assets' / relative
                except ValueError:
                    destination = ROOT / 'dist/assets' / ('order-' + uuid.uuid4().hex + path.suffix.lower())
                # Draft photographs stay outside the public output until approved.
                if not entry['approved'] and destination != path:
                    raise ValueError('Untuk mengimpor foto baru, centang persetujuan publikasi terlebih dahulu. Foto draft tidak disalin ke dist.')
                if destination != path:
                    shutil.copy2(path, destination)
                entry['photos'].append({'image': destination.relative_to(ROOT / 'dist').as_posix(), 'alt': alt or f"Foto {index + 1} pesanan {entry['title']}"})
            updated = copy.deepcopy(self.data)
            if self.current is None:
                updated.setdefault('progress', []).append(entry)
            else:
                updated['progress'][self.current] = entry
            self.persist(updated)
            self.delete_button.state(['!disabled'])
            self.current = next(i for i, record in enumerate(updated['progress']) if record['id'] == entry['id'])
            self.photos = [(ROOT / 'dist' / photo['image'], photo['alt']) for photo in entry['photos']]
            self.refresh()
            self.orders.current(self.current)
            messagebox.showinfo('Tersimpan', 'Pesanan disimpan. Cadangan: content/site.backup.json. Unggah ulang isi dist untuk memperbarui situs online. Foto lama tidak dihapus otomatis.')
        except Exception as error:
            messagebox.showerror('Belum tersimpan', str(error))

    def persist(self, updated):
        if SOURCE.read_bytes() != self.source_bytes:
            raise ValueError('Data diubah di luar panel. Tutup dan buka ulang panel agar perubahan tidak tertimpa.')
        public = compiler.compile_site(updated)
        output = ROOT / 'dist/content.js'
        old_output = output.read_bytes()
        source_temp = SOURCE.with_suffix('.tmp')
        output_temp = output.with_suffix('.tmp')
        try:
            source_temp.write_text(json.dumps(updated, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            # Preserve the existing content.js structure. Only update the progress section.
            # Contact, socials, projects, and steps must remain untouched.
            existing_output = output.read_text(encoding='utf-8') if output.exists() else ""
            marker = '"progress":'
            if marker not in existing_output:
                raise ValueError('Bagian progress tidak ditemukan pada content.js.')
            start = existing_output.index(marker) + len(marker)
            array_start = existing_output.index('[', start)

            depth = 0
            array_end = None
            in_string = False
            escaped = False
            for position in range(array_start, len(existing_output)):
                char = existing_output[position]
                if in_string:
                    if escaped:
                        escaped = False
                    elif char == '\\\\':
                        escaped = True
                    elif char == '"':
                        in_string = False
                else:
                    if char == '"':
                        in_string = True
                    elif char == '[':
                        depth += 1
                    elif char == ']':
                        depth -= 1
                        if depth == 0:
                            array_end = position + 1
                            break

            if array_end is None:
                raise ValueError('Format progress pada content.js tidak valid.')

            progress_json = json.dumps(public.get('progress', []), ensure_ascii=False, indent=2)
            new_output = existing_output[:array_start] + progress_json + existing_output[array_end:]
            output_temp.write_text(new_output, encoding='utf-8')
            shutil.copy2(SOURCE, SOURCE.with_name('site.backup.json'))
            source_temp.replace(SOURCE)
            try:
                output_temp.replace(output)
            except Exception:
                SOURCE.write_bytes(self.source_bytes)
                output.write_bytes(old_output)
                raise
        finally:
            source_temp.unlink(missing_ok=True)
            output_temp.unlink(missing_ok=True)
        self.data = updated
        self.source_bytes = SOURCE.read_bytes()

    def delete(self):
        if self.current is None:
            return
        entry = self.data['progress'][self.current]
        if not messagebox.askyesno('Hapus pesanan',
                f"Hapus pesanan '{entry['title']}' ({entry.get('projectCode', '')})?\n\n"
                'Pesanan akan dihapus dari data dan situs lokal. Perubahan formulir belum tersimpan akan diabaikan. '
                'Cadangan dibuat sebelum penghapusan. Foto tetap disimpan.'):
            return
        try:
            updated = copy.deepcopy(self.data)
            del updated['progress'][self.current]
            self.persist(updated)
            self.refresh()
            self.new(confirm=False)
            messagebox.showinfo('Pesanan dihapus',
                'Pesanan berhasil dihapus. Cadangan: content/site.backup.json. '
                'Unggah ulang isi dist agar pesanan juga hilang dari situs online. Foto tidak dihapus otomatis.')
        except Exception as error:
            messagebox.showerror('Belum terhapus', str(error))

    def close(self):
        if messagebox.askyesno('Tutup panel', 'Tutup panel? Perubahan formulir yang belum disimpan akan hilang.'):
            self.window.destroy()


if __name__ == '__main__':
    window = tk.Tk()
    Editor(window)
    window.mainloop()
