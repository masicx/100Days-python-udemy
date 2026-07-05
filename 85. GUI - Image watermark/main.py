"""
Watermark Studio - Desktop GUI application
--------------------------------------------
Upload an image and add a text or logo watermark to it, with live
preview, adjustable opacity/size/position, and the ability to save
the result.

Requirements:
    pip install pillow

Run with:
    python watermark_app.py
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox

from PIL import Image, ImageDraw, ImageFont, ImageTk


MAX_PREVIEW_SIZE = (700, 550)

POSITIONS = [
    "Top-Left", "Top-Center", "Top-Right",
    "Center-Left", "Center", "Center-Right",
    "Bottom-Left", "Bottom-Center", "Bottom-Right",
    "Tile (repeat)",
]


def find_a_font(size):
    """Try a few common truetype fonts before falling back to default."""
    candidates = [
        "arial.ttf", "Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


class WatermarkApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermark Studio")
        self.geometry("1050x680")
        self.minsize(900, 600)

        self.original_image = None      # PIL.Image, the loaded photo
        self.logo_image = None          # PIL.Image, the loaded logo
        self.result_image = None        # PIL.Image, photo + watermark
        self.preview_photo = None       # ImageTk.PhotoImage for canvas
        self.image_path = None
        self.logo_path = None

        # Tk variables
        self.watermark_type = tk.StringVar(value="text")
        self.text_value = tk.StringVar(value="Your Watermark")
        self.font_size = tk.IntVar(value=42)
        self.opacity = tk.IntVar(value=60)
        self.logo_scale = tk.IntVar(value=25)
        self.position = tk.StringVar(value="Bottom-Right")
        self.text_color = "#FFFFFF"
        self.status_text = tk.StringVar(value="Load an image to begin.")

        self._build_layout()

    # ------------------------------------------------------------------
    # Layout
    # ------------------------------------------------------------------
    def _build_layout(self):
        root = ttk.Frame(self, padding=10)
        root.pack(fill="both", expand=True)

        # Left: controls panel
        controls = ttk.Frame(root, width=300)
        controls.pack(side="left", fill="y", padx=(0, 10))

        ttk.Button(controls, text="1. Open Image...",
                   command=self.load_image).pack(fill="x", pady=4)

        ttk.Separator(controls).pack(fill="x", pady=8)

        ttk.Label(controls, text="Watermark Type",
                  font=("Segoe UI", 10, "bold")).pack(anchor="w")
        type_row = ttk.Frame(controls)
        type_row.pack(fill="x", pady=4)
        ttk.Radiobutton(type_row, text="Text", value="text",
                        variable=self.watermark_type,
                        command=self._refresh_option_panels).pack(side="left", padx=(0, 10))
        ttk.Radiobutton(type_row, text="Logo image", value="logo",
                        variable=self.watermark_type,
                        command=self._refresh_option_panels).pack(side="left")

        ttk.Separator(controls).pack(fill="x", pady=8)

        # --- Text options ---
        self.text_frame = ttk.Frame(controls)
        ttk.Label(self.text_frame, text="Watermark Text").pack(anchor="w")
        text_entry = ttk.Entry(self.text_frame, textvariable=self.text_value)
        text_entry.pack(fill="x", pady=(2, 8))
        text_entry.bind("<KeyRelease>", lambda e: self.update_preview())

        ttk.Label(self.text_frame, text="Font Size").pack(anchor="w")
        ttk.Scale(self.text_frame, from_=10, to=150, variable=self.font_size,
                  command=lambda e: self.update_preview()).pack(fill="x", pady=(2, 8))

        ttk.Button(self.text_frame, text="Choose Text Color...",
                   command=self.choose_color).pack(fill="x", pady=(0, 8))

        # --- Logo options ---
        self.logo_frame = ttk.Frame(controls)
        ttk.Button(self.logo_frame, text="Select Logo Image...",
                   command=self.load_logo).pack(fill="x", pady=(0, 8))
        ttk.Label(self.logo_frame, text="Logo Size (% of photo width)").pack(anchor="w")
        ttk.Scale(self.logo_frame, from_=5, to=80, variable=self.logo_scale,
                  command=lambda e: self.update_preview()).pack(fill="x", pady=(2, 8))

        # --- Shared options ---
        shared = ttk.Frame(controls)
        shared.pack(fill="x", pady=(4, 0))

        ttk.Label(shared, text="Opacity (%)").pack(anchor="w")
        ttk.Scale(shared, from_=10, to=100, variable=self.opacity,
                  command=lambda e: self.update_preview()).pack(fill="x", pady=(2, 8))

        ttk.Label(shared, text="Position").pack(anchor="w")
        position_menu = ttk.Combobox(shared, textvariable=self.position,
                                      values=POSITIONS, state="readonly")
        position_menu.pack(fill="x", pady=(2, 8))
        position_menu.bind("<<ComboboxSelected>>", lambda e: self.update_preview())

        self._refresh_option_panels()

        ttk.Separator(controls).pack(fill="x", pady=8)
        ttk.Button(controls, text="Save Watermarked Image...",
                   command=self.save_image).pack(fill="x", pady=4)

        # Right: preview canvas
        preview_area = ttk.Frame(root)
        preview_area.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(preview_area, bg="#2b2b2b", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        status_bar = ttk.Label(self, textvariable=self.status_text,
                                relief="sunken", anchor="w", padding=4)
        status_bar.pack(fill="x", side="bottom")

    def _refresh_option_panels(self):
        if self.watermark_type.get() == "text":
            self.logo_frame.pack_forget()
            self.text_frame.pack(fill="x")
        else:
            self.text_frame.pack_forget()
            self.logo_frame.pack(fill="x")
        self.update_preview()

    # ------------------------------------------------------------------
    # File operations
    # ------------------------------------------------------------------
    def load_image(self):
        path = filedialog.askopenfilename(
            title="Choose an image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
                       ("All files", "*.*")],
        )
        if not path:
            return
        try:
            image = Image.open(path).convert("RGBA")
        except Exception as exc:
            messagebox.showerror("Could not open image", str(exc))
            return
        self.original_image = image
        self.image_path = path
        self.status_text.set(f"Loaded: {os.path.basename(path)}  "
                              f"({image.width}x{image.height}px)")
        self.update_preview()

    def load_logo(self):
        path = filedialog.askopenfilename(
            title="Choose a logo image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif *.webp"),
                       ("All files", "*.*")],
        )
        if not path:
            return
        try:
            logo = Image.open(path).convert("RGBA")
        except Exception as exc:
            messagebox.showerror("Could not open logo", str(exc))
            return
        self.logo_image = logo
        self.logo_path = path
        self.update_preview()

    def choose_color(self):
        rgb, hex_color = colorchooser.askcolor(color=self.text_color,
                                                title="Choose watermark text color")
        if hex_color:
            self.text_color = hex_color
            self.update_preview()

    def save_image(self):
        if self.result_image is None:
            messagebox.showwarning("Nothing to save", "Load an image first.")
            return
        path = filedialog.asksaveasfilename(
            title="Save watermarked image",
            defaultextension=".png",
            filetypes=[("PNG image", "*.png"), ("JPEG image", "*.jpg")],
        )
        if not path:
            return
        to_save = self.result_image
        if path.lower().endswith((".jpg", ".jpeg")):
            to_save = to_save.convert("RGB")
        try:
            to_save.save(path)
        except Exception as exc:
            messagebox.showerror("Could not save image", str(exc))
            return
        self.status_text.set(f"Saved to: {path}")
        messagebox.showinfo("Saved", "Watermarked image saved successfully.")

    # ------------------------------------------------------------------
    # Watermark rendering
    # ------------------------------------------------------------------
    def _positions_for(self, canvas_size, item_size, tile=False):
        """Return list of (x, y) top-left coords for the watermark item."""
        cw, ch = canvas_size
        iw, ih = item_size
        margin = max(10, int(min(cw, ch) * 0.03))
        choice = self.position.get()

        if choice == "Tile (repeat)":
            coords = []
            step_x = iw + margin * 3
            step_y = ih + margin * 3
            y = margin
            while y < ch:
                x = margin
                while x < cw:
                    coords.append((x, y))
                    x += step_x
                y += step_y
            return coords

        slots = {
            "Top-Left": (margin, margin),
            "Top-Center": ((cw - iw) // 2, margin),
            "Top-Right": (cw - iw - margin, margin),
            "Center-Left": (margin, (ch - ih) // 2),
            "Center": ((cw - iw) // 2, (ch - ih) // 2),
            "Center-Right": (cw - iw - margin, (ch - ih) // 2),
            "Bottom-Left": (margin, ch - ih - margin),
            "Bottom-Center": ((cw - iw) // 2, ch - ih - margin),
            "Bottom-Right": (cw - iw - margin, ch - ih - margin),
        }
        return [slots.get(choice, slots["Bottom-Right"])]

    def _render_watermarked(self, base_image):
        """Return a new RGBA image with the watermark applied."""
        image = base_image.convert("RGBA")
        overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
        opacity_frac = max(0, min(100, self.opacity.get())) / 100.0

        if self.watermark_type.get() == "text":
            text = self.text_value.get().strip() or "Watermark"
            size = max(1, self.font_size.get())
            font = find_a_font(size)
            draw = ImageDraw.Draw(overlay)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

            r = int(self.text_color[1:3], 16)
            g = int(self.text_color[3:5], 16)
            b = int(self.text_color[5:7], 16)
            alpha = int(255 * opacity_frac)

            for (x, y) in self._positions_for(image.size, (text_w, text_h)):
                draw.text((x - bbox[0], y - bbox[1]), text,
                          font=font, fill=(r, g, b, alpha))

        else:  # logo
            if self.logo_image is None:
                return image
            scale_pct = max(1, self.logo_scale.get())
            target_w = max(1, int(image.width * scale_pct / 100))
            ratio = target_w / self.logo_image.width
            target_h = max(1, int(self.logo_image.height * ratio))
            logo_resized = self.logo_image.resize((target_w, target_h),
                                                    Image.LANCZOS)

            alpha_channel = logo_resized.split()[3].point(
                lambda a: int(a * opacity_frac)
            )
            logo_resized.putalpha(alpha_channel)

            for (x, y) in self._positions_for(image.size, (target_w, target_h)):
                overlay.paste(logo_resized, (x, y), logo_resized)

        return Image.alpha_composite(image, overlay)

    def update_preview(self):
        if self.original_image is None:
            return
        self.result_image = self._render_watermarked(self.original_image)

        preview = self.result_image.copy()
        preview.thumbnail(MAX_PREVIEW_SIZE, Image.LANCZOS)
        self.preview_photo = ImageTk.PhotoImage(preview)

        self.canvas.delete("all")
        self.canvas.update_idletasks()
        cw = self.canvas.winfo_width() or MAX_PREVIEW_SIZE[0]
        ch = self.canvas.winfo_height() or MAX_PREVIEW_SIZE[1]
        self.canvas.create_image(cw // 2, ch // 2, image=self.preview_photo,
                                  anchor="center")


if __name__ == "__main__":
    app = WatermarkApp()
    app.mainloop()