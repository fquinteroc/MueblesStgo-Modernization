import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EmpleadoListComponent } from './empleados/empleado-list/empleado-list.component';
import { DataUploadComponent } from './data/data-upload/data-upload.component';
import { MenuPrincipalComponent } from './menu-principal/menu-principal.component';

const routes: Routes = [
  { path: '', component: MenuPrincipalComponent },
  { path: 'empleados', component: EmpleadoListComponent },
  { path: 'data-upload', component: DataUploadComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
