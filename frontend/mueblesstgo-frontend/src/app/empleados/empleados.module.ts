import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { EmpleadoListComponent } from './empleado-list/empleado-list.component';
import { EmpleadoCreateComponent } from './empleado-create/empleado-create.component';
import { EmpleadoService } from './empleado.service';

@NgModule({
  declarations: [
    EmpleadoListComponent,
    EmpleadoCreateComponent
  ],
  imports: [
    CommonModule,
    FormsModule
  ],
  providers: [EmpleadoService],
  exports: [
    EmpleadoListComponent,
    EmpleadoCreateComponent
  ]
})
export class EmpleadosModule { }