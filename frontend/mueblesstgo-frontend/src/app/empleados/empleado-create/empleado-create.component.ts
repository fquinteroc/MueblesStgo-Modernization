import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { EmpleadoService } from '../empleado.service';
import { EmpleadoRequest } from '../empleado';

@Component({
  selector: 'app-empleado-create',
  templateUrl: './empleado-create.component.html',
  styleUrls: ['./empleado-create.component.css']
})
export class EmpleadoCreateComponent {
  empleado: EmpleadoRequest = {
    rut: '',
    nombres: '',
    apellidos: '',
    fecha_nacimiento: '',
    fecha_ingreso: '',
    categoria: 'A'
  };

  isSubmitting: boolean = false;
  errorMessage: string = '';
  successMessage: string = '';

  constructor(
    private empleadoService: EmpleadoService,
    private router: Router
  ) { }

  onSubmit(): void {
    if (!this.validateForm()) {
      return;
    }

    this.isSubmitting = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.empleadoService.crearEmpleado(this.empleado).subscribe({
      next: (empleadoCreado) => {
        this.successMessage = `Empleado ${empleadoCreado.nombres} ${empleadoCreado.apellidos} creado exitosamente.`;
        this.isSubmitting = false;
        
        // Redirigir después de 2 segundos
        setTimeout(() => {
          this.router.navigate(['/empleados']);
        }, 2000);
      },
      error: (error) => {
        this.errorMessage = error.message;
        this.isSubmitting = false;
      }
    });
  }

  validateForm(): boolean {
    if (!this.empleado.rut.trim()) {
      this.errorMessage = 'El RUT es obligatorio.';
      return false;
    }

    if (!this.empleado.nombres.trim()) {
      this.errorMessage = 'Los nombres son obligatorios.';
      return false;
    }

    if (!this.empleado.apellidos.trim()) {
      this.errorMessage = 'Los apellidos son obligatorios.';
      return false;
    }

    if (!this.empleado.fecha_nacimiento) {
      this.errorMessage = 'La fecha de nacimiento es obligatoria.';
      return false;
    }

    if (!this.empleado.fecha_ingreso) {
      this.errorMessage = 'La fecha de ingreso es obligatoria.';
      return false;
    }

    // Validar que la fecha de nacimiento no sea futura
    const birthDate = new Date(this.empleado.fecha_nacimiento);
    const today = new Date();
    if (birthDate > today) {
      this.errorMessage = 'La fecha de nacimiento no puede ser futura.';
      return false;
    }

    // Validar que la fecha de ingreso no sea futura
    const hireDate = new Date(this.empleado.fecha_ingreso);
    if (hireDate > today) {
      this.errorMessage = 'La fecha de ingreso no puede ser futura.';
      return false;
    }

    // Validar que el empleado sea mayor de edad al momento del ingreso
    const age = hireDate.getFullYear() - birthDate.getFullYear();
    if (age < 18) {
      this.errorMessage = 'El empleado debe ser mayor de edad al momento del ingreso.';
      return false;
    }

    return true;
  }

  formatRut(): void {
    // Formatear RUT automáticamente
    let rut = this.empleado.rut.replace(/[^0-9kK]/g, '');
    if (rut.length > 1) {
      rut = rut.slice(0, -1) + '-' + rut.slice(-1);
    }
    this.empleado.rut = rut.toUpperCase();
  }

  volverListado(): void {
    this.router.navigate(['/empleados']);
  }

  volverMenu(): void {
    this.router.navigate(['/']);
  }

  resetForm(): void {
    this.empleado = {
      rut: '',
      nombres: '',
      apellidos: '',
      fecha_nacimiento: '',
      fecha_ingreso: '',
      categoria: 'A'
    };
    this.errorMessage = '';
    this.successMessage = '';
  }
}
