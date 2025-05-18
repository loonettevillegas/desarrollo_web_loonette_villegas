

document.addEventListener('DOMContentLoaded', function() {
    const activitiesBody = document.getElementById('activities-body'); 
    const prevButton = document.getElementById('prev-boton');
    const nextButton = document.getElementById('post-boton');
    const currentPageSpan = document.getElementById('Pagina-actual');

    let currentPage = parseInt(currentPageSpan.textContent);
    let totalPages = parseInt('{{ total_pages }}');

    function fetchAndDisplayActivities(page) {
        fetch(`/actividades_paginadas?page=${page}`)
            .then(response => response.json())
            .then(data => {
                activitiesBody.innerHTML = ''; 
                totalPages = data.total_pages;
                currentPage = data.current_page;

                data.actividades.forEach(activity => {
                    const row = activitiesBody.insertRow(); 
                    row.style.cursor = 'pointer';
                    row.onclick = function() {
                        verDetalle(activity.id);
                    };
                    row.insertCell().textContent = activity.Inicio;
                    row.insertCell().textContent = activity.Termino;
                    row.insertCell().textContent = activity.Comuna;
                    row.insertCell().textContent = activity.Sector;
                    row.insertCell().textContent = activity.Tema;
                    row.insertCell().textContent = activity['Nombre organizador'];
                    const fotoCell = row.insertCell();
                    fotoCell.innerHTML = `<img src="${activity['Total fotos']}" alt="Foto" style="max-width: 100px; max-height: 100px;">`;
                });

                currentPageSpan.textContent = currentPage;
                prevButton.disabled = currentPage === 1;
                nextButton.disabled = currentPage === totalPages;
            })
            .catch(error => {
                console.error("Error al cargar las actividades:", error);
            });
    }

    function nextPage() {
        if (currentPage < totalPages) {
            fetchAndDisplayActivities(currentPage + 1);
        }
    }

    function prevPage() {
        if (currentPage > 1) {
            fetchAndDisplayActivities(currentPage - 1);
        }
    }
 function verDetalle(actividadId) {
 
        window.location.href = `/detalle/${actividadId}`;
        
    }

    nextButton.addEventListener('click', nextPage);
    prevButton.addEventListener('click', prevPage);

    fetchAndDisplayActivities(currentPage);
});