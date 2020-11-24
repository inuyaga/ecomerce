const codigos={'800044556':'Insumos Pedido Mensual','800044563':'Papeleria Pedido Mensual'}
function genrar_pdf_pedidos() {
    var url = '/pedido/pedidos/genera/pdf/';
    var data = { fecha_inicio: $('#fecha_init').val(), fecha_fin:$('#fecha_fin').val() };

    fetch(url, {
        method: 'POST', // or 'PUT'
            body: JSON.stringify(data),
            headers: {
                //   'Accept': 'application/json',
                'Content-Type': 'application/json',
                "X-CSRFToken": Cookies.get('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'include'
    }).then(res => res.json())
        .catch(error => console.error('Error:', error))
        .then(response => {
            // console.log('Success:', response)
            if (response.status) {
                renderiza_pdf(response.obj_list)
            }else{
                swal("Error!", response.msn, "warning");
            }
        });
}

function renderiza_pdf(items) {
    
    var doc = new jsPDF();
    var txt='';
    var arreglo=[]

    $.each( items, function( key, value ) {
        txt = `
        N° Pedido: ${value.ped_id_ped}      N° Pedido Computel: \n                    
        N° de Sucursal: ${value.ped_id_Suc__suc_numero} \n
        Nombre de Sucursal: ${value.ped_id_Suc__suc_nombre} \n
        Dirección de Sucursal: ${value.ped_id_Suc__suc_direccion} \n
        Codigo: ${value.pedido_tipo_insumo} ${codigos[value.pedido_tipo_insumo]}\n
        Informacion de Contacto: Edith Raquel Perera Hdez ext. 1003 \n
        Zona Referencia ${value.ped_id_Suc__suc_zona_str} \n
        `;
        data={"id":txt}
        arreglo.push(data)
      });

      var columns = [
        {title: "Etiketas para pedidos", key: "id"}, 
    ];
   
doc.autoTable(columns, arreglo, {});
doc.save('a4.pdf')
}

function get_array(params) {
    
}
