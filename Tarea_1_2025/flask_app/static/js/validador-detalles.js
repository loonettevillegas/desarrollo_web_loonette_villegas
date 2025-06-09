document.querySelectorAll('.Image-container img').forEach(image=>{
image.onclick = ()=>{document.querySelector('.popup-im').style.display = "block";
document.querySelector('.popup-im img').src = image.getAttribute('src')


}
});

document.querySelector('.popup-im span').onclick = () =>{
document.querySelector('.popup-im').style.display = 'none';


}
const validateAnyText = (text,x,y) => {
  if(!text) return false;
  let lengthValid = text.trim().length >= x && text.trim().length <= y;
  
  return lengthValid;
}       



document.addEventListener('DOMContentLoaded', function() {
    const commentForm = document.getElementById('second-form'); 
    const nameInput = document.getElementById('name_input');
    const comentarioInput = document.getElementById('comentario-input');
    const submitButton = document.getElementById('submit-btn');
    const listaComentarios = document.getElementById('lista-comentarios'); 
    
    function id() {
        const pathParts = window.location.pathname.split('/');
        
        const idIndex = pathParts.indexOf('detalle') + 1;
        if (idIndex > 0 && idIndex < pathParts.length) {
            return parseInt(pathParts[idIndex]);
        }
        return null; 
    }

    
    async function validarComentario() {
        const nombre = nameInput.value.trim();
        const comentarioTexto = comentarioInput.value.trim();
        const actividadId = id();

        let isValid = true;
        let errorMessage = '';


        if(!validateAnyText(nombre, 3 , 80)){
            isValid = false;
            errorMessage += 'El nombre debe tener entre 3 y 80 caracteres.\n';
        
        }
        if(!validateAnyText(comentarioTexto, 6 , 1000000)){
        isValid = false;
            errorMessage += 'El comentario debe tener  al menos 5 caracteres.\n';
        
        }
       
        if (!isValid) {
            popupFail();
            console.error('Errores de validación:', errorMessage);
            return; 
        }

    

        
        submitButton.disabled = true;
        submitButton.textContent = 'Enviando...';

        try {
            
            const formData = new FormData();
            
            formData.append('Nombre comentador', nombre);
            formData.append('comentarioinput', comentarioTexto);

          
            const response = await fetch(`/detalle/${actividadId}`, {
                method: 'POST', 
                body: formData 
            
            });

          
            

           
            const data = await response.json();

           
            if (data.success) {
                popupExito();
                nameInput.value = ''; 
                comentarioInput.value = ''; 
                await mostrarComentarios();
                
               
            } else {
                
                popupFail();
                console.error('Error del servidor:', data.message);
            }

        } catch (error) {
            console.error('Error al enviar el comentario:', error);
            popupFail();
        } finally {
           
            submitButton.disabled = false;
            submitButton.textContent = 'Agregar comentario';
        }
    }

    
    commentForm.addEventListener('submit', async function(event) {
        event.preventDefault(); 
        await validarComentario(); 
    });


     function seccionComentarios(comentarios) {
        listaComentarios.innerHTML = '';

        if (comentarios.length === 0) {
            listaComentarios.innerHTML = '<p>¡Sé el primero en comentar!</p>';
        } else {
            comentarios.forEach(comentario => {
                const commentDiv = document.createElement('div');
                commentDiv.classList.add('single-comment');

                commentDiv.innerHTML = `
                    <p><strong>${comentario.nombre}</strong> <span class="comment-date">(${comentario.fecha})</span></p>
                    <p>${comentario.texto}</p>
                `;
                listaComentarios.appendChild(commentDiv);
            });
        }
    }


    async function mostrarComentarios() {
        const actividadId = id();

        listaComentarios.innerHTML = '<p>Cargando comentarios...</p>'; 

        try {
           
            const comentariosData = await fetchAJAX(`/todos_los_comentarios/${actividadId}`);
            
            seccionComentarios(comentariosData);

        } catch (error) {
            console.error('Error al cargar los comentarios:', error);
            listaComentarios.innerHTML = '<p>Error al cargar los comentarios. Inténtalo de nuevo más tarde.</p>';
        }
    }

        mostrarComentarios();

});

//popups para saber si el comentario se envio o no
 function popupExito() {
        const exitoPopup = document.querySelector(".popup-exito"); 
 
        exitoPopup.style.display = "flex";
        setTimeout(() => {
            exitoPopup.style.display = "none";
        }, 2000);
}

function popupFail() {
        const failPopup = document.querySelector(".popup-fail");          
        failPopup.style.display = "flex"; 
        setTimeout(() => {
            failPopup.style.display = "none";
        }, 3000); 
}

//función del aux para obtener los comentarios

let fetchAJAX = (url) => {
        return fetch(url, {
            mode: "cors",
            credentials: "include",
        })
        .then((response) => {
            if (!response.ok) {
                throw new Error(`Network response was not ok, status: ${response.status}`);
            }
            return response.json(); 
        });
   
    };