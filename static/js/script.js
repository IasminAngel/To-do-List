document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function (e) {
      const inputs = this.querySelectorAll("input[required]");
      let isValid = true;

      inputs.forEach(input => {
        if (!input.value.trim()) {
          isValid = false;
          input.style.border = "1px solid red";
        } else {
          input.style.border = "";
        }
      });

      if (!isValid) {
        e.preventDefault();
        alert("Preencha todos os campos obrigatórios!");
      }
    });
  });
});

document.querySelectorAll(".form-edicao").forEach((form) => {
  form.addEventListener("submit", function (event) {
    const ano = this.querySelector("input[name='ano']").value;
    if (ano < 1900 || ano > new Date().getFullYear()) {
      event.preventDefault();
      alert("Ano inválido! Digite um ano entre 1900 e o ano atual.");
    }
  });
});

function setupTableButtons() {
  document.querySelectorAll(".remover").forEach((btn) => {
    btn.replaceWith(btn.cloneNode(true));
  });
  document.querySelectorAll(".alterar").forEach((btn) => {
    btn.replaceWith(btn.cloneNode(true));
  });

  document.querySelectorAll(".remover").forEach((button) => {
    button.addEventListener("click", function () {
      let idCarro = this.getAttribute("data-id");
      if (
        confirm(`Tem certeza que deseja excluir o carro com ID ${idCarro}?`)
      ) {
        fetch("/deletar_carro", {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: idCarro }),
        })
          .then((response) => {
            if (!response.ok) throw new Error("Erro na requisição");
            return response.json();
          })
          .then((data) => {
            alert(data.mensagem);
            location.reload();
          })
          .catch((error) => {
            console.error("Erro:", error);
            alert("Erro ao remover carro");
          });
      }
    });
  });

  document.querySelectorAll(".alterar").forEach((button) => {
    button.addEventListener("click", function () {
      let idCarro = this.getAttribute("data-id");
      let placa = this.getAttribute("data-placa");
      let marca = this.getAttribute("data-marca");
      let modelo = this.getAttribute("data-modelo");
      let ano = this.getAttribute("data-ano");

      document.getElementById("idCarro").value = idCarro;
      document.getElementById("placa").value = placa;
      document.getElementById("marca").value = marca;
      document.getElementById("modelo").value = modelo;
      document.getElementById("ano").value = ano;

      document.getElementById("formEdicao").style.display = "block";
      document.getElementById("tabelaCarros").style.display = "none";
    });
  });
}

document
  .getElementById("cancelarEdicao")
  .addEventListener("click", function () {
    document.getElementById("formEdicao").style.display = "none";
    document.getElementById("tabelaCarros").style.display = "block";
  });

document
  .getElementById("formAlterar")
  .addEventListener("submit", async function (event) {
    event.preventDefault();

    const idCarro = document.getElementById("idCarro").value;
    const placa = document.getElementById("placa").value;
    const marca = document.getElementById("marca").value;
    const modelo = document.getElementById("modelo").value;
    const ano = document.getElementById("ano").value;

    try {
      const response = await fetch("/alterar_carro", {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id: idCarro,
          placa: placa,
          marca: marca,
          modelo: modelo,
          ano: ano,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.mensagem || "Erro ao alterar carro");
      }

      alert(data.mensagem);
      location.reload();
    } catch (error) {
      console.error("Erro:", error);
      alert(error.message);
    }
  });

document.getElementById('exibir-carros').addEventListener('click', function (e) {
  e.preventDefault();
  const tabela = document.getElementById('tabelaCarros');
  tabela.style.display = tabela.style.display === 'none' ? 'block' : 'none';
});

document.querySelectorAll('.btn-remover').forEach(btn => {
  btn.addEventListener('click', function () {
    const idCarro = this.getAttribute('data-id');
    if (confirm('Tem certeza que deseja remover este carro?')) {
      fetch('/deletar_carro', {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id: idCarro })
      })
        .then(response => response.json())
        .then(data => {
          alert(data.mensagem);
          window.location.reload();
        })
        .catch(error => {
          console.error('Error:', error);
          alert('Erro ao remover carro');
        });
    }
  });
});

document.querySelector('form[action="/registrar_entrada"]').addEventListener('submit', function (e) {
  const placa = this.querySelector('input[name="placa"]').value.trim();
  if (!placa) {
    e.preventDefault();
    alert('Por favor, informe a placa do carro');
  }
});

document.querySelectorAll('form[action="/registrar_saida"]').forEach(form => {
  form.addEventListener('submit', function (e) {
    e.preventDefault();

    if (confirm('Confirmar saída do veículo?')) {
      const formData = new FormData(this);

      fetch(this.action, {
        method: 'POST',
        body: formData
      })
        .then(response => {
          if (response.redirected) {
            window.location.href = response.url;
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('Erro ao registrar saída');
        });
    }
  });
});

function atualizarListaCarros() {
  fetch('/exibir_carro')
    .then(response => response.text())
    .then(html => {
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const novaTabela = doc.getElementById('tabelaCarros');
      document.getElementById('tabelaCarros').replaceWith(novaTabela);
    })
    .catch(error => console.error('Erro:', error));
}

document.querySelector('form[action="/registrar_carro"]').addEventListener('submit', function () {
  setTimeout(atualizarListaCarros, 500);
});
