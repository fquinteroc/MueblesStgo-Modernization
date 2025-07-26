import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EmpleadoListComponent } from './empleados/empleado-list/empleado-list.component';
import { EmpleadoCreateComponent } from './empleados/empleado-create/empleado-create.component';
import { DataUploadComponent } from './data/data-upload/data-upload.component';
import { DataListComponent } from './data/data-list/data-list.component';
import { MenuPrincipalComponent } from './menu-principal/menu-principal.component';

const routes: Routes = [
  { path: '', component: MenuPrincipalComponent },
  { path: 'empleados', component: EmpleadoListComponent },
  { path: 'empleados/crear', component: EmpleadoCreateComponent },
  { path: 'data-upload', component: DataUploadComponent },
  { path: 'data-list', component: DataListComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
