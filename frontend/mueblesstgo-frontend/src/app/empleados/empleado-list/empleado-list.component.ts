import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Empleado } from '../empleado';
import { EmpleadoService } from '../empleado.service';

@Component({
  selector: 'app-empleado-list',
  templateUrl: './empleado-list.component.html',
  styleUrls: ['./empleado-list.component.css']
})
export class EmpleadoListComponent implements OnInit {
  empleados: Empleado[] = [];

  constructor(private empleadoService: EmpleadoService, private router: Router) { }

  getEmpleados(): void {
    this.empleadoService.getEmpleados().subscribe((empleados) => {
      this.empleados = empleados;
    });
  }

  volverMenu(): void {
    this.router.navigate(['/']);
  }

  ngOnInit() {
    this.getEmpleados();
  }
}