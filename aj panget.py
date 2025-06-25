import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont
import os


class DigitalResumeApp:
    def __init__(self, master):
        self.master = master
        if isinstance(self.master, (ctk.CTk, ctk.CTkToplevel)):
            self.master.title("Digital Resume - Aj S. Lorenzo")
        self.master.attributes('-fullscreen', True)
        self.master.bind("<Escape>", lambda event: self.master.attributes("-fullscreen", not self.master.attributes("-fullscreen")))

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.primary_bg = "#F3E5F5"
        self.secondary_bg = "#E1BEE7"
        self.text_color_dark = "#4A148C"
        self.text_color_light = "#AB47BC"
        self.accent_color = "#8E24AA"
        self.line_color = "#CE93D8"
        self.border_color = "#BA68C8"

        full_name_parts = "AJ S LORENZO".split()
        self.personal_info = {
            "LAST_NAME": full_name_parts[-1],
            "FIRST_NAME": full_name_parts[0],
            "MIDDLE_NAME": full_name_parts[1].replace('.', '') if len(full_name_parts) > 2 and full_name_parts[1].endswith('.') else (full_name_parts[1] if len(full_name_parts) > 2 else "S"),
            "CONTACT_NUM": "+63 967 458 3299",
            "EMAIL": "ajsampol08@gmail.com",
            "ADDRESS": "Pandacan, Metro Manila",
        }

        self.profile_details = {
            "Gender": "Male",
            "Date of Birth": "October 8, 2005",
            "Age": "19",
            "Civil Status": "Single",
            "Citizenship": "Filipino",
        }

        self.skills = [
            "Time Management",
            "Problem-Solving",
            "Team Player",
            "Punctual",
            "Adaptability"
        ]

        self.education = [
            {"level": "SENIOR HIGH SCHOOL", "institution": "Manuel A. Roxas Highschool",
             "years": "2022-2024"},
            {"level": "COLLEGE", "institution": 'Eulogio "Amang" Rodriguez Institute of Science and Technology',
             "years": "2024-Present"}
        ]

        self.master.after(100, self._create_layout)

    def _create_layout(self):
        main_resume_container = ctk.CTkFrame(self.master,
                                             fg_color=self.primary_bg,
                                             corner_radius=10,
                                             border_color=self.border_color,
                                             border_width=2)
        main_resume_container.pack(fill="both", expand=True, padx=20, pady=20)

        main_grid_frame = ctk.CTkFrame(main_resume_container, fg_color="transparent")
        main_grid_frame.pack(fill="both", expand=True, padx=10, pady=10)

        main_grid_frame.grid_rowconfigure(0, weight=1)
        main_grid_frame.grid_rowconfigure(1, weight=2)
        main_grid_frame.grid_columnconfigure(0, weight=1)
        main_grid_frame.grid_columnconfigure(1, weight=1)

        info_name_contact_frame = ctk.CTkFrame(main_grid_frame, fg_color="transparent")
        info_name_contact_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        info_name_contact_frame.grid_rowconfigure(0, weight=1)
        info_name_contact_frame.grid_rowconfigure(1, weight=1)
        info_name_contact_frame.grid_columnconfigure(0, weight=1)

        name_display_frame = ctk.CTkFrame(info_name_contact_frame, fg_color="transparent")
        name_display_frame.pack(fill="both", expand=True, pady=(0, 10))

        full_name_display = (
            f"{self.personal_info['LAST_NAME']}, {self.personal_info['FIRST_NAME']}"
            f"{' ' + self.personal_info['MIDDLE_NAME'] if self.personal_info['MIDDLE_NAME'] else ''}"
        )
        ctk.CTkLabel(name_display_frame, text=full_name_display,
                     font=("Arial", 28, "bold"),
                     text_color=self.text_color_dark,
                     anchor="w", justify="left", wraplength=int(self.master.winfo_screenwidth() * 0.45)).pack(fill="x", pady=2)


        contact_frame = ctk.CTkFrame(name_display_frame, fg_color="transparent")
        contact_frame.pack(fill="x", pady=(15, 0))

        self._add_contact_item(contact_frame, "📞", self.personal_info["CONTACT_NUM"])
        self._add_contact_item(contact_frame, "✉️", self.personal_info["EMAIL"])
        ctk.CTkFrame(contact_frame, height=1, fg_color=self.line_color).pack(fill="x", pady=10)
        self._add_contact_item(contact_frame, "🏠", self.personal_info["ADDRESS"],
                               wraplength=int(self.master.winfo_screenwidth() * 0.35))

        photo_frame = ctk.CTkFrame(main_grid_frame, fg_color="transparent")
        photo_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=0)
        photo_frame.grid_rowconfigure(0, weight=1)
        photo_frame.grid_columnconfigure(0, weight=1)

        try:
            script_dir = os.path.dirname(__file__)
            image_path = os.path.join(script_dir, 'ajlorenzo.jpg')

            if not os.path.exists(image_path):
                img_pil = Image.new('RGB', (250, 250), color='#E1BEE7')
                draw = ImageDraw.Draw(img_pil)
                try:
                    font = ImageFont.truetype("arial.ttf", 100)
                except IOError:
                    font = ImageFont.load_default()
                draw.text((50, 75), "ASL", fill=self.text_color_light, font=font)
                img_pil.save(image_path)

            img = Image.open(image_path)
            img = img.resize((250, 250), Image.Resampling.LANCZOS)
            self.profile_photo = ctk.CTkImage(light_image=img, dark_image=img, size=(250, 250))
            profile_label = ctk.CTkLabel(photo_frame, image=self.profile_photo, text="")
            profile_label.pack(expand=True, anchor="center")
        except Exception as e:
            ctk.CTkLabel(photo_frame, text="[Profile Image]", text_color=self.text_color_light,
                         font=("Arial", 18)).pack(expand=True, anchor="center")

        profile_edu_frame = ctk.CTkFrame(main_grid_frame, fg_color="transparent")
        profile_edu_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        profile_edu_frame.grid_columnconfigure(0, weight=1)

        self._create_section_with_header(profile_edu_frame, "PROFILE", self.profile_details.items())

        edu_items = []
        for edu in self.education:
            edu_items.append((edu["level"], edu["institution"]))
            edu_items.append((f"Years: {edu['years']}", ""))
            edu_items.append(("", ""))

        self._create_section_with_header(profile_edu_frame, "EDUCATION", edu_items, is_list_format=True)

        skills_frame = ctk.CTkFrame(main_grid_frame, fg_color="transparent")
        skills_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        skills_frame.grid_columnconfigure(0, weight=1)

        skills_items = [(f"• {skill}", "") for skill in self.skills]
        self._create_section_with_header(skills_frame, "SKILLS", skills_items, is_list_format=True)

    def _add_contact_item(self, parent_frame, icon, text_content, wraplength=None):
        item_frame = ctk.CTkFrame(parent_frame, fg_color="transparent")
        item_frame.pack(fill="x", pady=6)

        ctk.CTkLabel(item_frame, text=icon, font=("Arial", 20, "bold"),
                     text_color=self.accent_color).pack(side="left", anchor="n", padx=(0, 10))

        if wraplength:
            ctk.CTkLabel(item_frame, text=text_content, font=("Arial", 18),
                         text_color=self.text_color_dark, wraplength=wraplength, justify="left").pack(side="left", anchor="w")
        else:
            ctk.CTkLabel(item_frame, text=text_content, font=("Arial", 18),
                         text_color=self.text_color_dark).pack(side="left", anchor="w")

    def _create_section_with_header(self, parent_frame, title, data, is_list_format=False):
        header_frame = ctk.CTkFrame(parent_frame, fg_color=self.secondary_bg, corner_radius=0)
        header_frame.pack(fill="x", pady=(20, 0), padx=(0, 0))
        ctk.CTkLabel(header_frame, text=title, font=("Arial", 22, "bold"),
                     text_color=self.text_color_dark, anchor="w").pack(padx=25, pady=10)

        ctk.CTkFrame(parent_frame, height=2, fg_color=self.accent_color).pack(fill="x", padx=25, pady=(0, 10))

        content_frame = ctk.CTkFrame(parent_frame, fg_color=self.primary_bg)
        content_frame.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        column_content_wraplength = int(self.master.winfo_screenwidth() * 0.45) - 50
        if column_content_wraplength < 200:
            column_content_wraplength = 200

        for item_key, item_value in data:
            if is_list_format:
                if item_key and not item_value:
                    ctk.CTkLabel(content_frame, text=item_key, font=("Arial", 16),
                                 text_color=self.text_color_dark, wraplength=column_content_wraplength,
                                 justify="left").pack(anchor="w", pady=2)
                elif item_key and item_value:
                    ctk.CTkLabel(content_frame, text=item_key, font=("Arial", 16, "bold"),
                                 text_color=self.text_color_dark, wraplength=column_content_wraplength, justify="left").pack(anchor="w",
                                                                                                 pady=(8, 0))
                    ctk.CTkLabel(content_frame, text=item_value, font=("Arial", 15),
                                 text_color=self.text_color_light, wraplength=column_content_wraplength, justify="left").pack(anchor="w")
                elif not item_key and not item_value:
                    ctk.CTkFrame(content_frame, height=10, fg_color="transparent").pack()
            else:
                info_row = ctk.CTkFrame(content_frame, fg_color="transparent")
                info_row.pack(fill="x", pady=3)
                ctk.CTkLabel(info_row, text=f"{item_key}:", font=("Arial", 16, "bold"),
                             text_color=self.text_color_dark).pack(side="left", anchor="w", padx=(0, 10))
                ctk.CTkLabel(info_row, text=item_value, font=("Arial", 16),
                             text_color=self.text_color_light).pack(side="left", anchor="w")


if __name__ == "__main__":
    root = ctk.CTk()
    app = DigitalResumeApp(root)
    root.mainloop()