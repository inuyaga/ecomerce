

  <!-- Content Wrapper. Contains page content -->
  <div class="content-wrapper">
    <!-- Content Header (Page header) -->
    <section class="content-header">
      <h1>
        Administrar
        <small>Informes</small>
      </h1>
      <ol class="breadcrumb">
        <li><a href="#"><i class="fa fa-dashboard"></i>Inicio</a></li>
        <li class="active">Informes</li>
      </ol>
    </section>

    <!-- Main content -->
    <section class="content">
      <!-- Small boxes (Stat box) -->
      <div class="row">
        <div class="col-md-12 col-xs-12">

          <?php if($this->session->flashdata('success')): ?>
            <div class="alert alert-success alert-dismissible" role="alert">
              <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
              <?php echo $this->session->flashdata('success'); ?>
            </div>
          <?php elseif($this->session->flashdata('error')): ?>
            <div class="alert alert-error alert-dismissible" role="alert">
              <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
              <?php echo $this->session->flashdata('error'); ?>
            </div>
          <?php endif; ?>
          
          <?php if(in_array('createUser', $user_permission)): ?>
            <a href="<?php echo base_url('users/create') ?>" class="btn btn-primary">Agregar usuario</a>
            <br /> <br />
          <?php endif; ?>


          <div class="box">
            <div class="box-header">
              <h3 class="box-title">Administrar informes <?php echo $this->session->userdata('seccion') ?></h3>
            </div>
            <!-- /.box-header -->
            <div class="box-body table-responsive">
              <table id="userTable" class="table table-bordered table-striped">
                <thead>
                <tr>
                    <th>#</th>
                    <th>Tutor(es)</th>
                    <th>Alumno</th>
                    <th>Tel</th>
                    <th>Correo</th>
                    <th>Nivel</th>
                    <th>Fecha</th>
                    <th>Doc</th>
                    <th>Razón</th>
                    <th>Se enteró</th>
                    <th>Proviene</th>
                    <th>Enviar inf</th>

                  <?php if(in_array('updateInforme', $user_permission) || in_array('deleteInforme', $user_permission)): ?>
                  <th>Acción</th>
                  <?php endif; ?>
                </tr>
                </thead>
                <tbody>
                  <?php if($informe_data): ?>                  
                    <?php foreach ($informe_data as $k => $v): 
                      $img=explode("/",$v['user_info']['ruta_img']);
                      $pdf=explode(".",end($img));
                      ?>
                      <tr>
                        <td><?php echo $v['user_info']['id']; ?></td>
                        <td><?php echo $v['user_info']['nombreT'].' / '.$v['user_info']['nombreT2']; ?></td>
                        <td><?php echo $v['user_info']['nombreA'] .' / '. $v['user_info']['nombreA2'].' / '. $v['user_info']['nombreA3']; ?></td>
                        <td><?php echo $v['user_info']['telefono']; ?></td>
                        <td><?php echo $v['user_info']['email']; ?></td>
                        <td><?php echo $v['user_info']['nivelE']; ?></td>
                        <td><?php echo $v['user_info']['fecha_adicion']; ?></td>
                        <?php
                            if(strtolower(end($pdf)) == "pdf"){ ?>
                              <td><a href="http://colegiomexicodelsureste.edu.mx/publico/images/R_costos/<?php echo end($img) ?>" target="_blank"><img src="https://play-lh.googleusercontent.com/u9ofV9e2diX3giScuXT46B4A0vxFw8tj5NzHQJVAqAKwL5b_o8CHnO-qiZZIZYHlTg" width="150" height="150" class="img-circle"></a></td>
                        <?php
                            }else{ ?>
                              <td><a href="http://colegiomexicodelsureste.edu.mx/publico/images/R_costos/<?php echo end($img) ?>" target="_blank"><img src="http://colegiomexicodelsureste.edu.mx/publico/images/R_costos/<?php echo end($img) ?>" width="150" height="150" class="img-circle"></a></td>
                        <?php
                            }
                            
                        ?>
                        <td><?php echo $v['user_info']['razon']; ?></td>
                        <td><?php echo $v['user_info']['donde_supo']; ?></td>
                        <td><?php echo $v['user_info']['proviene']; ?></td>
                        <td>Enviado: <?= $v['user_info']['Enviado'] ?><br><a href="<?= base_url('informes/EnviarCostos/'.$v['user_info']['id']) ?>">Enviar Información</a></td>
                        <?php if(in_array('updateInforme', $user_permission) || in_array('deleteInforme', $user_permission)): ?>

                        <td>
                          <!-- <?php if(in_array('updateInforme', $user_permission)): ?>
                            <a href="<?php echo base_url('informes/edit/'.$v['user_info']['id']) ?>" class="btn btn-default"><i class="fa fa-edit"></i></a>
                          <?php endif; ?> -->
                          <?php if(in_array('deleteInforme', $user_permission)): ?>
                            <a href="<?php echo base_url('informes/delete/'.$v['user_info']['id']) ?>" class="btn btn-default"><i class="fa fa-trash"></i></a>
                          <?php endif; ?>
                        </td>
                      <?php endif; ?>
                      </tr>
                    <?php endforeach ?>
                  <?php endif; ?>
                </tbody>
              </table>
            </div>
            <!-- /.box-body -->
          </div>
          <!-- /.box -->
        </div>
        <!-- col-md-12 -->
      </div>
      <!-- /.row -->
      

    </section>
    <!-- /.content -->
  </div>
  <!-- /.content-wrapper -->

  <script type="text/javascript">
    $(document).ready(function() {
      $('#userTable').DataTable({
        "aoColumns": [
            { "orderSequence": [ "desc" ] },
            null,
            null,
            null,
            null,
            null
        ]
    } );

      $("#mainInformeNav").addClass('active');
      $("#manageInformeNav").addClass('active');
    });
  </script>
