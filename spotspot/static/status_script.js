const socket = io();
const cancelActive = document.getElementById('cancel-active-button');
const cancelAll = document.getElementById('cancel-all-button');

window.onload = function () {
    socket.emit("get_status");
};

socket.on("update_status", function (data) {
    const historyContainer = document.getElementById("history-body");
    historyContainer.innerHTML = "";

    if (data.history.length === 0) {
        document.getElementById("no-downloads-msg").style.display = "block";
    } else {
        document.getElementById("no-downloads-msg").style.display = "none";
        data.history.forEach(function (item) {
            const row = document.createElement("tr");

            const nameCell = document.createElement("td");
            nameCell.textContent = item.name;
            row.appendChild(nameCell);

            const typeCell = document.createElement("td");
            typeCell.textContent = item.type;
            row.appendChild(typeCell);

            const artistCell = document.createElement("td");
            artistCell.textContent = item.artist;
            row.appendChild(artistCell);

            const urlCell = document.createElement("td");
            const urlLink = document.createElement("a");
            urlLink.href = item.url;
            urlLink.textContent = item.url;
            urlLink.target = "_blank";
            urlCell.appendChild(urlLink);
            row.appendChild(urlCell);

            const statusCell = document.createElement("td");
            statusCell.textContent = item.status;
            row.appendChild(statusCell);

            historyContainer.appendChild(row);
        });
    }
});

cancelActive.addEventListener('click', function () {
    socket.emit("cancel_active");
});

cancelAll.addEventListener('click', function () {
    socket.emit("cancel_all");
});
