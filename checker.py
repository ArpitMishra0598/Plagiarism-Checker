import os
import re
import difflib
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext


def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def calculate_similarity(text1, text2):
    seq = difflib.SequenceMatcher(None, text1, text2)
    return round(seq.ratio() * 100, 2)


def detailed_comparison(text1, text2):
    seq = difflib.SequenceMatcher(None, text1, text2)
    matches = seq.get_matching_blocks()
    report = []
    for match in matches:
        if match.size > 0:
            report.append(text1[match.a: match.a + match.size])
    return report


def check_plagiarism(folder_path, text_widget):
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]

    if not files:
        messagebox.showwarning("No Files", "No .txt files found in the selected folder.")
        return

    file_contents = {}
    for file in files:
        with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
            file_contents[file] = clean_text(f.read())

    report_lines = []
    text_widget.delete(1.0, tk.END)  # Clear previous results
    text_widget.insert(tk.END, "📑 Plagiarism Report\n" + "-" * 60 + "\n")

    for i in range(len(files)):
        for j in range(i + 1, len(files)):
            sim = calculate_similarity(file_contents[files[i]], file_contents[files[j]])
            result_line = f"{files[i]}  <-->  {files[j]}  :  {sim}% similar\n"
            text_widget.insert(tk.END, result_line)

            report_lines.append(result_line)
            common_parts = detailed_comparison(file_contents[files[i]], file_contents[files[j]])
            if common_parts:
                text_widget.insert(tk.END, "   Common content snippets:\n")
                report_lines.append(" Common content snippets:\n")
                for part in common_parts[:5]:
                    snippet_line = f"     - {part}\n"
                    text_widget.insert(tk.END, snippet_line)
                    report_lines.append(snippet_line)
            text_widget.insert(tk.END, "-" * 60 + "\n")
            report_lines.append("-" * 60 + "\n")

    # Save report to file
    report_path = os.path.join(folder_path, "detailed_report.txt")
    with open(report_path, "w", encoding="utf-8") as f:
        f.writelines(report_lines)

    messagebox.showinfo("Report Generated", f"✅ Detailed report saved at:\n{report_path}")


def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        check_plagiarism(folder_path, output_text)


# Tkinter GUI setup
root = tk.Tk()
root.title("Plagiarism Checker")
root.geometry("700x500")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

label = tk.Label(frame, text="Select a folder containing .txt files", font=("Arial", 12))
label.pack(pady=5)

browse_button = tk.Button(frame, text="Browse Folder", command=browse_folder, bg="lightblue")
browse_button.pack(pady=5)

output_text = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=80, height=20, font=("Courier New", 10))
output_text.pack(pady=10, fill="both", expand=True)

root.mainloop()
