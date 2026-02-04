function showPage(id) {
    document.querySelectorAll(".page")
        .forEach(p => p.classList.remove("active"));

    document.getElementById(id).classList.add("active");
}

function startDetect() {
    fetch("http://localhost:5000/detect")
        .then(res => res.json())
        .then(data => {
            document.getElementById("menuName").innerText =
                data.menu || "ไม่สามารถระบุเมนูได้";

            document.getElementById("weightValue").innerText =
                data.weight_gram + " g";

            document.getElementById("priceValue").innerText =
                data.price_baht + " บาท";

            document.getElementById("totalPrice").innerText =
                data.price_baht;

            showPage("page-result");
        })
        .catch(err => {
            console.error(err);
            alert("ตรวจจับล้มเหลว");
        });
}

function confirmFood() {
    showPage("page-done");

    let timeLeft = 5;
    const cooldownText = document.getElementById("cooldownText");

    cooldownText.innerText = `จะกลับสู่หน้าแรกภายใน ${timeLeft} วินาที`;

    const countdown = setInterval(() => {
        timeLeft--;

        if (timeLeft > 0) {
            cooldownText.innerText = `จะกลับสู่หน้าแรกภายใน ${timeLeft} วินาที`;
        } else {
            clearInterval(countdown);
            resetApp();
        }
    }, 1000);
}

function resetApp() {
    showPage("page-start");
}
