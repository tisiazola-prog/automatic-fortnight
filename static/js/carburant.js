// Variable pour stocker tous les véhicules
$(document).ready(function () {


    $(function () {
        carburant_data();
        filtreCarburants();
    });




    // RECUPERATION DES TOUS LES VEHICULES
    function carburant_data() {

        $.ajax({
            type: "GET",  // Méthode GET recommandée pour récupérer des données
            url: "/api/carburants",
            dataType: "json",  // Spécifie le type de données attendu en réponse
            success: function (response) {
                // Traitement des données reçues
                if (response && response.length > 0) {
                    allVehicules = response; // Stocke tous les véhicules
                    display_carburants(response);
                    console.log(response);


                } else {
                    console.log("Aucun gestion de carburant trouvé");
                    
                }
            },
            error: function (xhr, status, error) {
                console.error("Erreur AJAX :", status, error);
                alert("Erreur lors de la récupération des carburants");
            }
        });
    }


    function display_carburants(carburants) {
        let content = '';

        if (carburants.length === 0) {
            content = `
            <tr>
                <td colspan="9" class="no-results">Aucun carburant trouvé avec ces critères</td> 
            </tr>
        `;
        } else {
            carburants.forEach(carburant => {
                content += `
              <tr>
                <td>${new Date(carburant.date_ajout).toLocaleDateString()}</td>
                <td>${carburant.type}</td>
                <td>${carburant.marque}</td>
                <td>${carburant.litre.toFixed(2)} L</td>
                <td>${carburant.prix_litre.toFixed(2)} €</td>
                <td>${(carburant.litre * carburant.prix_litre).toFixed(2)} €</td>
                <td>${carburant.km_parcours} km</td>
                <td>${carburant.consomation.toFixed(2)} L/100km</td>
                  <td class="actions">
                      <button class="btn btn-sm btn-primary edit-vehicule" data-id="">
                          <i class="fas fa-edit"></i>
                      </button>
                      <button class="btn btn-sm btn-danger delete-vehicule" data-id="">
                          <i class="fas fa-trash"></i>
                      </button>
                  </td>
              </tr>
            `;
            });
        }

        $("#displayCarburants").html(content);
    }

    function filtreCarburants() {
        // Déclenchement lors de la soumission du formulaire, des changements dans les champs OU de la saisie dans marque
        $('#filtreForm').on('submit change', function (e) {
            e.preventDefault();
            lanceRecherche();
        });

        // Ajout de l'événement keyup sur le champ marque avec un délai anti-rebond
        $('#marque-filter').on('keyup', debounce(function () {
            lanceRecherche();
        }, 300));

        // Fonction qui lance la recherche
        function lanceRecherche() {
            const filters = {
                marque: $('#marque-filter').val()
            };

            // On n'ajoute 'type' que si une valeur est sélectionnée (pas "Tous")
            const type = $('#type-filter').val();
            if (type) filters.type = type;

            $.ajax({
                url: '/api/filtreVehicules',
                type: 'GET',
                data: filters,
                success: function (response) {
                    console.log("Réponse du serveur :", response);
                    display_vehicules(response);
                }
            });
        }

        // Fonction debounce pour limiter les appels AJAX
        function debounce(func, wait) {
            let timeout;
            return function () {
                const context = this, args = arguments;
                clearTimeout(timeout);
                timeout = setTimeout(function () {
                    func.apply(context, args);
                }, wait);
            };
        }
    }





});


