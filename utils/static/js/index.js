$(document).ready(function() {
    // Initialisation des modales
    $(".modal").hide();

    $(".modal-close").click(function() {
        $('.modal').fadeOut();
    })

    // Gestion des événements
    $('#loginBtn').click(() => $('#AddVehicule').fadeIn());

    $('.modal-clos').click(function() { $(this).closest('.modal').fadeOut(); });
    $(window).click(function(e) { if ($(e.target).hasClass('modal')) $('.modal').fadeOut(); });



    // Initialisation des fonctions principales
    initLoginForm();
    loadVehicles();
    initFilter();

    // Fonctions principales
    function loadVehicles() {
        $.get("/api/vehicules")
            .done(handleVehicleResponse)
            .fail(handleAjaxError);
    }

    function initFilter() {
        $('#filtreForm').on('submit change', preventSubmit);
        $('#marque-filter').on('keyup', debounce(searchVehicles, 300));
    }

    function initLoginForm() {
        $('#loginForm').submit(handleLogin);
    }

    // Fonctions utilitaires
    function handleVehicleResponse(response) {
        const vehicles = response.data || response;
        displayVehicles(Array.isArray(vehicles) ? vehicles : []);
    }

    function displayVehicles(vehicles) {
        const container = $('#vehiclesContainer');
        container.empty();

        if (!vehicles.length) {
            container.html('<p class="no-vehicles">Aucun véhicule disponible</p>');
            return;
        }

        vehicles.forEach(v => {
            container.append(`
                <div class="vehicle-card" data-id="${v.id}" data-type="${v.type}">
                    <img src="/static/upload/${v.image}" class="vehicle-img">
                    <div class="vehicle-info">
                        <h3>${v.marque || 'Marque non spécifiée'}</h3>
                        <p class="model">${v.model || 'Modèle inconnu'}</p>
                        <button class="see-more-btn voirePlus" data-id="${v.id}" data-type="${v.type}">Voir plus</button>
                    </div>
                </div>
            `);
        });

        initDetailButtons();
    }

    function searchVehicles() {
        const filters = {
            marque: $('#marque-filter').val(),
            type: $('#type-filter').val() || undefined
        };

        $.get('/api/filtreVehicules', filters)
            .done(displayVehicles)
            .fail(handleAjaxError);
    }

    function initDetailButtons() {
        $(".voirePlus").click(function() {


            const btn = $(this);
            $('#vehiculeModalBoite').fadeIn();

            $.get("/api/showOneVehicule", {
                    vehicule_id: btn.data("id"),
                    vehicule_type: btn.data("type")
                }).done(showVehicleDetails)
                .fail(handleAjaxError);
        });
    }

    function showVehicleDetails(response) {
        if (response.error) return console.error(response.error);

        const container = $('#ModalVoirePlus');
        container.html(`
            <div class="modal-content">
                <span class="close-btn modal-close">&times;</span>
                <div class="entete">
                    <img src="/static/upload/${response.image || 'default.jpg'}" alt="${response.marque}">
                    <div class="infos">
                        <label>Type : <span>${response.type || 'Nom precisé'} </span></label>
                        <label>Marque : <span>${response.marque || 'Nom precisé'} </span>  </label>
                        <label>Modèle : <span>${response.model || 'Nom precisé'} </span> </label>
                        <label>Imatriculation :  <span>${response.immatriculation || 'Nom precisé'} </span></label>
                        <label>Année : <span>${response.annee || 'Nom precisé'} </span></label> 
                        <label>Capacité :  <span>${response.capacite || 'Nom precisé'} </span></label>
                        <label>Kilometrage : <span>${response.kilometrage || 'Nom precisé'} Km/H </span></label> 
                         <label>Statut : <span>${response.status || 'Nom precisé'} </span></label> 
                          <label>Date d'ajout : <span>${response.date || 'Nom precisé'} </span></label> 
                    </div>
                </div>
                <div class="pied">
                    <label>Nombre de place: <span>${response.places || 'N/A'}</span></label>
                    <div class="action">
                        <button class="res btnAction" data-action="0" data-id="${response.id}" >Modifier</button>
                        <button class="com btnAction" data-action="1" data-id="${response.id}" >Supprimer</button>
                    </div>
                </div>
            </div>
        `);

        $(".modal-close").click(function() { $(".modal").fadeOut() })
        $(".Message").hide();
        initActions();

    }


    function handleLogin(e) {
        e.preventDefault();
        const formData = {
            fullName: $('#fullName').val(),
            phone: $('#phone').val(),
            address: $('#address').val()
        };

        console.log('Login attempt:', formData);
        alert('Merci! Nous vous contacterons bientôt.');
        $(this).trigger('reset').closest('.modal').fadeOut();
    }

    function handleAjaxError(xhr) {
        const error = xhr.responseJSON;
        console.error(`Erreur ${xhr.status}:`, error);
        alert(`Erreur serveur (${xhr.status}). Veuillez réessayer.`);
    }

    function debounce(func, wait) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    function preventSubmit(e) {
        e.preventDefault();
        searchVehicles();
    }

    function initActions() {
        $(document).on('click', '.btnAction', function() {

            $.get("/api/action", {
                    action: $(this).data("action"),
                    vehicule_id: $(this).data("id")
                })
                .done(showActionResponse)
                .fail(handleAjaxError);
        });
    }

    function showActionResponse(response) {
        const vehicleModal = $("#vehicleModal");



        // Nettoyer avant d'ajouter
        vehicleModal.find('.Message').remove();

        vehicleModal.append(`
        <div class="Message">
            <span class="close-btn close">&times;</span>
            <h3>Votre <span>${response}</span> a été envoyé avec succès</h3>
            <p>Veuillez passer à notre bureau pour finaliser</p>
        </div>
    `);

        // Animation et gestion de la fermeture
        $(".Message").hide().fadeIn();

        $('.close').off('click').on('click', function() {
            $(this).closest('.Message').fadeOut(function() {
                $(this).remove();
            });
        });

        // Fermer automatiquement après 5s
        setTimeout(() => {
            $('.Message').fadeOut();
        }, 5000);
    }
});