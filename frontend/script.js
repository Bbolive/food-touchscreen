function showPage(id) {
    document.querySelectorAll(".page").forEach(p => p.classList.remove("active"));
    document.getElementById(id).classList.add("active");
}

function startDetect() {
    fetch("http://localhost:5000/detect")
        .then(res => res.json())
        .then(data => {
            document.getElementById("menuName").innerText =
                data[0]?.food || "ไม่สามารถระบุเมนูได้";

            showPage("page-result");
        })
        .catch(() => alert("ตรวจจับล้มเหลว"));
}

function confirmFood() {
    showPage("page-done");

    setTimeout(() => {
        resetApp();
    }, 5000);
}

function resetApp() {
    showPage("page-start");
}
