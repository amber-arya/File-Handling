# ============================================================
#  File Handling System
#  Built with: Python + Streamlit + Pathlib
#  Author: [Amber Arya]
# ============================================================

import streamlit as st
from pathlib import Path

# ── Page setup ──────────────────────────────────────────────
st.set_page_config(
    page_title="File Handling System",
    page_icon="🗂️",
    layout="centered",
)

# ── Load external CSS ────────────────────────────────────────
def load_css(file_path):
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("style.css")

# ── Storage folder ───────────────────────────────────────────
# All files the user creates will live inside this folder
FILES_DIR = Path("files")
FILES_DIR.mkdir(exist_ok=True)   # create if it doesn't exist yet


# ── Helper: full path for a filename ─────────────────────────
def get_path(filename: str) -> Path:
    """Return the full Path object for a file inside FILES_DIR."""
    return FILES_DIR / filename.strip()


# ── Helper: list files in storage ────────────────────────────
def list_files() -> list[str]:
    """Return sorted list of filenames inside FILES_DIR."""
    return sorted([f.name for f in FILES_DIR.iterdir() if f.is_file()])


# ═══════════════════════════════════════════════════════════
#  SIDEBAR NAVIGATION
# ═══════════════════════════════════════════════════════════
st.sidebar.markdown('<div class="sidebar-title">🗂️ File System</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-sub">Choose an operation</div>', unsafe_allow_html=True)
st.sidebar.markdown("---")

menu = st.sidebar.radio(
    label="Navigation",
    options=["📄 Create File", "🔍 Read File", "✏️ Update File", "🗑️ Delete File"],
    label_visibility="collapsed",
)

# Show how many files are stored
total = len(list_files())
st.sidebar.markdown("---")
st.sidebar.markdown(f'<div class="sidebar-count">📁 {total} file(s) stored</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════
#  MAIN HEADER
# ═══════════════════════════════════════════════════════════
st.markdown('<div class="main-title">File Handling System</div>', unsafe_allow_html=True)
st.markdown('<div class="main-sub">Create · Read · Update · Delete files using Python & Pathlib</div>', unsafe_allow_html=True)
st.markdown("---")


# ═══════════════════════════════════════════════════════════
#  PAGE 1 — CREATE FILE
# ═══════════════════════════════════════════════════════════
if menu == "📄 Create File":

    st.markdown('<div class="section-title">📄 Create a New File</div>', unsafe_allow_html=True)
    st.markdown("Enter a filename and write your content below. The file will be saved inside the `files/` folder.")
    st.markdown("")

    filename = st.text_input("File Name", placeholder="e.g. notes.txt")
    content  = st.text_area("File Content", placeholder="Write your content here...", height=180)

    if st.button("✅ Create File"):
        if not filename.strip():
            st.error("⚠️ Please enter a file name.")
        else:
            path = get_path(filename)
            if path.exists():
                st.error(f"❌ File **{filename}** already exists. Try a different name.")
            else:
                try:
                    # Write the content into the new file
                    path.write_text(content, encoding="utf-8")
                    st.success(f"✅ File **{filename}** created successfully inside `files/`!")
                except Exception as err:
                    st.error(f"❌ Something went wrong: {err}")


# ═══════════════════════════════════════════════════════════
#  PAGE 2 — READ FILE
# ═══════════════════════════════════════════════════════════
elif menu == "🔍 Read File":

    st.markdown('<div class="section-title">🔍 Read a File</div>', unsafe_allow_html=True)
    st.markdown("Select a file from the list to view its contents.")
    st.markdown("")

    files = list_files()

    if not files:
        st.info("📭 No files found. Go to **Create File** to add one first.")
    else:
        selected = st.selectbox("Choose a file", files)

        if st.button("📖 Read File"):
            path = get_path(selected)
            try:
                content = path.read_text(encoding="utf-8")
                st.success(f"✅ Showing contents of **{selected}**")

                # Display the file content in a styled code block
                st.markdown('<div class="file-box">' + (content.replace("\n", "<br>") if content else "<i>(empty file)</i>") + '</div>', unsafe_allow_html=True)

                # Small file info row
                size = path.stat().st_size
                lines = len(content.splitlines())
                st.markdown(
                    f'<div class="file-meta">📦 Size: {size} bytes &nbsp;|&nbsp; 📝 Lines: {lines} &nbsp;|&nbsp; 🔤 Chars: {len(content)}</div>',
                    unsafe_allow_html=True
                )
            except Exception as err:
                st.error(f"❌ Could not read file: {err}")


# ═══════════════════════════════════════════════════════════
#  PAGE 3 — UPDATE FILE
# ═══════════════════════════════════════════════════════════
elif menu == "✏️ Update File":

    st.markdown('<div class="section-title">✏️ Update a File</div>', unsafe_allow_html=True)
    st.markdown("Pick a file and choose what you want to do with it.")
    st.markdown("")

    files = list_files()

    if not files:
        st.info("📭 No files found. Create a file first.")
    else:
        selected = st.selectbox("Choose a file to update", files)

        # Sub-operation picker
        operation = st.radio(
            "What do you want to do?",
            ["Rename File", "Append Content", "Overwrite Content"],
            horizontal=True,
        )

        st.markdown("")

        # ── Rename ──────────────────────────────────────────
        if operation == "Rename File":
            new_name = st.text_input("New File Name", placeholder="e.g. renamed.txt")

            if st.button("🔄 Rename"):
                if not new_name.strip():
                    st.error("⚠️ Please enter a new file name.")
                else:
                    old_path = get_path(selected)
                    new_path = get_path(new_name)

                    if new_path.exists():
                        st.error(f"❌ **{new_name}** already exists. Choose a different name.")
                    else:
                        try:
                            old_path.rename(new_path)
                            st.success(f"✅ Renamed **{selected}** → **{new_name}**")
                        except Exception as err:
                            st.error(f"❌ Rename failed: {err}")

        # ── Append ──────────────────────────────────────────
        elif operation == "Append Content":
            extra = st.text_area("Content to Append", placeholder="This will be added at the end of the file...", height=150)

            if st.button("➕ Append"):
                if not extra.strip():
                    st.error("⚠️ Please enter some content to append.")
                else:
                    path = get_path(selected)
                    try:
                        # Open in append mode — adds to end without erasing
                        with open(path, "a", encoding="utf-8") as f:
                            f.write("\n" + extra)
                        st.success(f"✅ Content appended to **{selected}** successfully!")
                    except Exception as err:
                        st.error(f"❌ Append failed: {err}")

        # ── Overwrite ────────────────────────────────────────
        elif operation == "Overwrite Content":
            st.warning("⚠️ This will replace the entire content of the file.")
            new_content = st.text_area("New Content", placeholder="Old content will be completely replaced...", height=150)

            if st.button("💾 Overwrite"):
                path = get_path(selected)
                try:
                    path.write_text(new_content, encoding="utf-8")
                    st.success(f"✅ **{selected}** has been overwritten successfully!")
                except Exception as err:
                    st.error(f"❌ Overwrite failed: {err}")


# ═══════════════════════════════════════════════════════════
#  PAGE 4 — DELETE FILE
# ═══════════════════════════════════════════════════════════
elif menu == "🗑️ Delete File":

    st.markdown('<div class="section-title">🗑️ Delete a File</div>', unsafe_allow_html=True)
    st.markdown("Select the file you want to delete. **This action cannot be undone.**")
    st.markdown("")

    files = list_files()

    if not files:
        st.info("📭 No files to delete. Your storage is empty.")
    else:
        selected = st.selectbox("Choose a file to delete", files)

        # Safety checkbox — so users don't delete by accident
        confirmed = st.checkbox(f'Yes, I want to permanently delete **{selected}**')

        if st.button("🗑️ Delete File"):
            if not confirmed:
                st.warning("⚠️ Please confirm by checking the box above.")
            else:
                path = get_path(selected)
                try:
                    path.unlink()   # delete the file
                    st.success(f"✅ **{selected}** has been deleted.")
                    st.rerun()      # refresh page so file disappears from list
                except Exception as err:
                    st.error(f"❌ Delete failed: {err}")


