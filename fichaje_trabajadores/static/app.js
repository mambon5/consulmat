// static/app.js

// Funció per obtenir els treballadors des del backend i mostrar-los
function mostrarTreballadors() {
    fetch('/treballadors')
        .then(response => {
            console.log("resposta:");
            console.log(response);
            // Comprovar si la resposta és exitosa
            if (!response.ok) {
              throw new Error('Error en la resposta del servidor');
            }
            // Comprovar el tipus de contingut
            const contentType = response.headers.get('Content-Type');
            if (contentType && contentType.includes('application/json')) {
              return response.json(); // Analitzar com JSON
            } else {
              throw new Error('La resposta no és JSON');
            }
          })
        .then(data => {
            console.log(data);
            const taulaBody = document.getElementById('taula-treballadors').getElementsByTagName('tbody')[0];
            taulaBody.innerHTML = '';  // Netegem la taula abans de mostrar noves dades

            data.forEach(treballador => {
                const fila = document.createElement('tr');

                const celNom = document.createElement('td');
                celNom.textContent = treballador.nom_i_cognom;
                fila.appendChild(celNom);

                const celDepartament = document.createElement('td');
                celDepartament.textContent = treballador.departament;
                fila.appendChild(celDepartament);

                const celCorreu = document.createElement('td');
                celCorreu.textContent = treballador.correu;
                fila.appendChild(celCorreu);

                const celData = document.createElement('td');
                celData.textContent = treballador.created_at;
                fila.appendChild(celData);

                taulaBody.appendChild(fila);
            });
        })
        .catch(error => console.error('Error al carregar els treballadors:', error));
}

// Quan la pàgina carregui, mostrar treballadors
window.onload = mostrarTreballadors;
