async function generateBrochure() {
    const company_name = document.getElementById("companyName").value.trim();
    const url = document.getElementById("companyUrl").value.trim();
  
    const runBtn = document.getElementById("runBtn");
    const loading = document.getElementById("loading");
    const errorMsg = document.getElementById("errorMsg");
    const outputWrap = document.getElementById("outputWrap");
    const brochureOutput = document.getElementById("brochureOutput");
  
    errorMsg.classList.remove("active");
    outputWrap.classList.remove("active");
  
    if (!company_name || !url) {
      errorMsg.textContent = "Enter both a company name and a URL before running the press.";
      errorMsg.classList.add("active");
      return;
    }
  
    runBtn.disabled = true;
    loading.classList.add("active");
  
    try {
      const res = await fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ company_name, url })
      });
  
      if (!res.ok) {
        throw new Error(`Server responded with ${res.status}`);
      }
  
      const data = await res.json();
      brochureOutput.innerHTML = marked.parse(data.brochure);
      outputWrap.classList.add("active");
    } catch (err) {
      errorMsg.textContent = "Couldn't generate the brochure. Check the URL and try again.";
      errorMsg.classList.add("active");
    } finally {
      runBtn.disabled = false;
      loading.classList.remove("active");
    }
  }