// Pobieranie danych z API i rysowanie tabeli
function renderTableFromAPI(url) {
  const table = document.getElementById("tabela_krypto");
  const header =
    "<tr><th>Nazwa</th> <th>Cena</th> <th>1 dzień</th> <th>7 dni</th> <th>ATH</th></tr>";
  fetch(url)
    .then((response) => response.json())
    .then(function (data) {
      let tablebody = header;
      for (let i = 0; i < Object.keys(data).length; i++) {
        let price = parseFloat(data[i].price).toFixed(2);
        let oneDayPrice = parseFloat(data[i]["1d"].price_change).toFixed(2);
        let sevenDaysPrice = parseFloat(data[i]["7d"].price_change).toFixed(2);
        let ATH = parseFloat(data[i].high).toFixed(2);
        let oneDayPerc = parseFloat(data[i]["1d"].price_change_pct).toFixed(2);
        let sevenDayPerc = parseFloat(data[i]["7d"].price_change_pct).toFixed(
          2
        );
        let tablerow = `
                <tr>
                <td>
                    <a href="../kryptowaluta/${data[i].id}"><img src="${
          data[i].logo_url
        }" style="width: 25px; height: 25px">
                    <span>${data[i].name} <span class="datawpisu">${
          data[i].symbol
        }</span></span></a>
                </td>
                <td>$${price.replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,")}</td>`;
        if (oneDayPrice >= 0) {
          tablerow += `<td style="color: green">&nbsp;${oneDayPrice.replace(
            /(\d)(?=(\d\d\d)+(?!\d))/g,
            "$1,"
          )} <span class="datawpisu">${oneDayPerc}%</span></td>`;
        } else {
          tablerow += `<td style="color: red">${oneDayPrice.replace(
            /(\d)(?=(\d\d\d)+(?!\d))/g,
            "$1,"
          )} <span class="datawpisu">${oneDayPerc}%</span></td>`;
        }
        if (sevenDaysPrice >= 0) {
          tablerow += `<td style="color: green">&nbsp;${sevenDaysPrice.replace(
            /(\d)(?=(\d\d\d)+(?!\d))/g,
            "$1,"
          )} <span class="datawpisu">${sevenDayPerc}%</span></td>`;
        } else {
          tablerow += `<td style="color: red">${sevenDaysPrice.replace(
            /(\d)(?=(\d\d\d)+(?!\d))/g,
            "$1,"
          )} <span class="datawpisu">${sevenDayPerc}%</span></td>`;
        }
        tablerow += `<td>$${ATH.replace(
          /(\d)(?=(\d\d\d)+(?!\d))/g,
          "$1,"
        )}</td></tr>`;
        tablebody += tablerow;
      }
      table.innerHTML = tablebody;
    });
}
