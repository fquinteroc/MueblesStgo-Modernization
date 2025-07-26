import { Injectable } from '@angular/core';
import { Empleado } from './empleado';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EmpleadoService {
  constructor() { }

  getEmpleados(): Observable<Empleado[]> {
    // Simulación de datos, reemplaza por llamada HTTP si tienes API
    const empleados: Empleado[] = [
      {
        id:1,
        rut: '12345678-9',
        apellidos: 'Pérez',
        nombres: 'Juan',
        fecha_nacimiento: '1990-01-01',
        categoria: 'A',
        fecha_ingreso: '2020-05-10'
      },
      {
        id:2,
        rut: '123-2',
        apellidos: 'Constanza',
        nombres: 'Oliva',
        fecha_nacimiento: '2001-11-18',
        categoria: 'C',
        fecha_ingreso: '2018-05-30'
      },

      // ...más empleados
    ];
    return of(empleados);
  }
}