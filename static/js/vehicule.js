$(document).ready(function() {

    $(".cylindre").hide();



    // Gestion de la sélection d'image
    $('button[for="file"]').click(function(e) {
        e.preventDefault();
        $('#file').click();
    });

    $('#file').change(function() {
        if (this.files && this.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('.boxImg img').attr('src', e.target.result);
            }
            reader.readAsDataURL(this.files[0]);
        }
    });


    $("#type").change(function(event) {

        if ($(event.target).val() == "Moto") {
            $(".cylindre").show();
        } else {
            $('#cylindre').val("");
            $(".cylindre").hide();


        }

    })

    // Soumission du formulaire
    $('#addVehiculeForms').submit(function(e) {
        e.preventDefault();

        // Créer FormData à partir du formulaire spécifique

        const type_vehicule = $('#type_vehicule').val().trim();
        const marque = $('#marque').val().trim();
        const modele = $('#modele').val().trim();
        const immatriculation = $('#immatriculation').val().trim();
        const annee = $('#annee').val().trim();
        const capacite = $('#capacite').val().trim();
        const nb_place = $('#nb_place').val().trim();
        const kilometrage = $('#kilometrage').val().trim();

        if (type_vehicule == "" || marque == "" || modele == "" || immatriculation == "" ||
            annee == "" || capacite == "" || nb_place == "" || kilometrage == "") {
            alert("Veuillez remplir tous les champs")

        } else {

            let formData = {
                type_vehicule: $('#type_vehicule').val().trim(),
                marque: $('#marque').val().trim(),
                modele: $('#modele').val().trim(),
                immatriculation: $('#immatriculation').val().trim(),
                annee: $('#annee').val().trim(),
                capacite: $('#capacite').val().trim(),
                nb_place: $('#nb_place').val().trim(),
                kilometrage: $('#kilometrage').val().trim(),


            };

            const cylindreValue = $('#cylindre').val().trim();
            if (cylindre !== "") {
                formData.cylindre = cylindreValue;
            }

            console.log(formData);



            $.ajax({
                url: '/ajouterVehicule',
                type: 'POST',
                processData: false,
                contentType: "application/json",
                data: JSON.stringify(formData),

                success: function(response) {
                    if (response.success == true) {
                        alert(response.message);
                        location.reload();

                    } else {
                        alert(response.message);

                    }
                },
                error: function(xhr, status, error) {
                    // Affiche les détails complets de l'erreur
                    console.error("Status:", status);
                    console.error("Error:", error);
                    console.error("Response:", xhr.responseText);

                    let errorMsg = "Erreur serveur";
                    try {
                        const serverResponse = JSON.parse(xhr.responseText);
                        errorMsg = serverResponse.message || serverResponse.error || errorMsg;
                    } catch (e) {}

                    alert('Erreur: ' + errorMsg + '\nCode: ' + xhr.status);
                }
            });

        }


    });

    // Annuler
    $('#Annuler').click(function(e) {
        e.preventDefault();
        $('form')[0].reset();
        $('.boxImg img').attr('src', "{{url_for('static', filename='upload/voiture1.jpg')}}");
    });
});