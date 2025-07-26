import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { EmpleadoListComponent } from './empleado-list/empleado-list.component';

@NgModule({
  declarations: [EmpleadoListComponent],
  imports: [CommonModule],
  exports: [EmpleadoListComponent]
})
export class EmpleadosModule { }