
//logica comunas 
document.addEventListener('DOMContentLoaded', function() {
    const regionSelect = document.getElementById('region');
    const comunaSelect = document.getElementById('comuna');

    comunaSelect.disabled = true;
    comunaSelect.innerHTML = '<option disabled selected value="0">Seleccione una comuna</option>';

    regionSelect.addEventListener('change', function() {
        const selectedRegionId = this.value;

        if (selectedRegionId !== '0') {
            fetch(`/informar-actividad?region=${selectedRegionId}`) 
                .then(response => response.json())
                .then(data => {
                    comunaSelect.disabled = false;
                    comunaSelect.innerHTML = '<option disabled selected value="0">Seleccione una comuna</option>';
                    data.forEach(comuna => {
                        const option = document.createElement('option');
                        option.value = comuna.id;
                        option.textContent = comuna.nombre;
                        comunaSelect.appendChild(option);
                    });
                })
                .catch(error => {
                    console.error('Error al cargar las comunas:', error);
                    comunaSelect.innerHTML = '<option disabled selected value="0">Error al cargar las comunas</option>';
                    comunaSelect.disabled = true;
                });
        } else {
            comunaSelect.disabled = true;
            comunaSelect.innerHTML = '<option disabled selected value="0">Seleccione una comuna</option>';
        }
    });
});

//logica contacto



//logica tema
    

//hidden value for theme description
 document.getElementById("theme_select_form").addEventListener("change", function() {
            let inputContainer = document.getElementById("Other-selection");
            if (this.value=="10") {
                inputContainer.style.display = "block"; 
            } else {
                inputContainer.style.display = "none";
            }
        });





/*hidden value for channel description*/
 document.getElementById("contact_select_form").addEventListener("change", function() {
            let inputContainer = document.getElementById("contact-selection");
            if (this.value) {
                inputContainer.style.display = "block"; 
            } else {
                inputContainer.style.display = "none";
            }
        });

const validateAnyText = (text,x,y) => {
  if(!text) return false;
  let lengthValid = text.trim().length >= x && text.trim().length <= y;
  
  return lengthValid;
}       

//funciones del aux
const validateName = (name) => {
  if(!name) return false;
  let lengthValid = name.trim().length >= 4 && name.trim().length <= 200;
  
  return lengthValid;
}

const validateEmail = (email) => {
  if (!email) return false;
  let lengthValid = email.length < 100 ;

  let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
  let formatValid = re.test(email);
  return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
  if (!phoneNumber) return false;
  let lengthValid = phoneNumber.length >= 8;

  let re = /^\+\d{3}\.\d{8}$/;
  let formatValid = re.test(phoneNumber);

  return lengthValid && formatValid;
};

const validateFiles = (files) => {
  if (!files) return false;
  let lengthValid = 1 <= files.length && files.length <= 5;
  let typeValid = true;
  for (const file of files) {
    let fileFamily = file.type.split("/")[0];
    typeValid &&= fileFamily == "image" || file.type == "application/pdf";
  }
  return lengthValid && typeValid;
};

const validateSelect = (select) => {
  if(!select) return false;
  return true;
}
const validate_regions = (index)=>{
    
    return index!=0 ;
}

const validate_comuna = (index)=>{
    return index>0;
}

const validateInitialDate = (date)=>{
 if (!date) return false;
 let re = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
 let formatValid = re.test(date);

return  formatValid;
 }
const validateFinalDate = (date1, date2) =>{
 if (!date2) return false;
 let re = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
 let formatValid = re.test(date2);
const d1 = new Date(date1);
const d2 = new Date(date2);
let validDate = d1<d2 ;
return  formatValid && validDate;
 }



const validateForm = (event)=> {

    event.preventDefault(); 
//extrayendo info
    let myForm = document.getElementById('first-form');;
    let email = myForm["email"].value;
    let phoneNumber = myForm["contacto"].value;
    let name = myForm["name_input"].value;
    let region_select= myForm["region"].selectedIndex;
    let comuna_select=myForm["comuna"].selectedIndex;
    let files = myForm["photo_1"].files;
    let theme = myForm["theme_select_form"].value;
    let time = myForm["date-initial-form"].value;
    let time2 = myForm["date-end-form"].value;
    let description_sector = myForm["sector_text"].value;
    let description_contact = myForm["contact_select_form"].value;
    let contact = myForm["contact_select_form"].value;
   



//listando invalida inputs
    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid &&= false;
    };

//revisando qué es inválido
    if(!validate_regions(region_select)){
            
            setInvalidInput("Región");
    }
        
    if(!validate_comuna(comuna_select)){
        setInvalidInput("Comuna");
            
    }

    if (!validateAnyText(description_sector,0,100)) {
        setInvalidInput("Descripción del sector");
        }
    if (!validateName(name)) {
            setInvalidInput("Nombre organizador");
    }
    
    if (!validateEmail(email)) {
            setInvalidInput("Email");
    }
    
    if (!validatePhoneNumber(phoneNumber)) {
            setInvalidInput("Número de contacto");

    }
    if(!validateSelect(contact)){
        setInvalidInput("Selección contacto");
    }
    if (validateSelect(contact)&&!validateAnyText(description_contact,4,50)){
        setInvalidInput("Descripción del contacto");
        }
        
     if(!validateInitialDate(time)){
        setInvalidInput("Fecha y tiempo de inicio");
            
        }
    if(!validateFinalDate(time,time2)){
        setInvalidInput("Fecha y tiempo de fin");
            
        }
    
    if (!validateSelect(theme)) {
        setInvalidInput("Tema");
        }
    
    if (!validateFiles(files)) {
            setInvalidInput("Fotos");
    }
            
    
   
    



  let validationBox = document.getElementById("val-box");
  let validationMessageElem = document.getElementById("val-msg");
  let validationListElem = document.getElementById("val-list");
        
    if (!isValid) {
            validationListElem.textContent = "";
            // agregar elementos inválidos al elemento val-list.
            for (input of invalidInputs) {
            let listElement = document.createElement("li");
            listElement.innerText = input;
            validationListElem.append(listElement);
            }
            // establecer val-msg
            validationMessageElem.innerText = "Los siguientes campos son inválidos:";

            // aplicar estilos de error
            validationBox.style.backgroundColor = "#ffdddd";
            validationBox.style.borderLeftColor = "#f44336";

            // hacer visible el mensaje de validación
            validationBox.hidden = false;
        } else {
          
            // Ocultar el formulario
           // myForm.style.display = "none";
            

           Popup1();
        }
        };

 function Popup1() {
  const firstPopup = document.getElementById("popup");
  firstPopup.style.display = "block";

  document.getElementById("confirmarButton").addEventListener("click", function() {
    firstPopup.style.display = "none"; 
   sendFormData();
  });

  document.getElementById("cancelarButton").addEventListener("click", function() {
    firstPopup.style.display = "none"; 
  });
}

function popup2() {
    console.log("Ejecutando popup2() simplificado");
    const secondPopup = document.getElementById("popup_confirmacion");
    if (secondPopup) {
        secondPopup.style.display = "block";
    } else {
        console.error("No se encontró popup_confirmacion");
    }
}    

function sendFormData() {
  const form = document.getElementById("first-form");
  const formData = new FormData(form);

  fetch("/informar-actividad", {
    method: "POST",
    body: formData,
  })
  
    .then((response) => response.json())
    .then((data) => {
    console.log("Data success:", data.success); 
      if (data.success) {
                  console.log("Llamando a popup2() desde sendFormData"); // Para confirmar que se intenta llamar

            popup2();
      } else {
        console.error("Error:", data.message);
      }
    })
    .catch((error) => {
      console.error("Fetch error:", error);
    alert("Ocurrió un error de conexión. Por favor, inténtelo de nuevo."); 

    });
    
}
let submitBtn = document.getElementById("submit-btn");
submitBtn.addEventListener("click", validateForm);