function detect() {
  fetch("http://localhost:5000/detect")
    .then((res) => res.json())
    .then((data) => {
      const resultDiv = document.getElementById("result");

      if (data.message) {
        resultDiv.innerHTML = data.message;
        return;
      }

      let html = "";
      data.forEach((item) => {
        html += `
                    <p><b>อาหาร:</b> ${item.food}</p>
                    <p><b>ความมั่นใจ:</b> ${(item.confidence * 100).toFixed(0)}%</p>
                    <hr>
                `;
      });

      html += `
                <button onclick="confirmFood()">ยืนยัน</button>
                <button onclick="cancelFood()">ยกเลิก</button>
            `;

      resultDiv.innerHTML = html;
    })
    .catch((err) => {
      document.getElementById("result").innerHTML = "เกิดข้อผิดพลาด";
      console.error(err);
    });
}

function confirmFood() {
  alert("ยืนยันรายการอาหาร");
}

function cancelFood() {
  document.getElementById("result").innerHTML = "กรุณาวางถาดอาหาร";
}
