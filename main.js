
const form = document.getElementById("uploadForm");
const result = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const fileInput = form.querySelector('input[name="excel"]');
  if (!fileInput.files.length) {
    result.textContent = "Please select a file";
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]); // <-- matches FastAPI parameter "file"

  try {
    const response = await fetch("http://127.0.0.1:8000/upload-excel/1", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errData = await response.json();
      throw new Error(errData.detail || "Unknown error");
    }

    const data = await response.json();
    result.textContent = JSON.stringify(data, null, 2);
  } catch (err) {
    result.textContent = "Upload failed: " + err.message;
  }
});

