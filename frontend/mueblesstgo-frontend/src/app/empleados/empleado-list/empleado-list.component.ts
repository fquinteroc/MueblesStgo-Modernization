import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Empleado, EmployeeListResponse } from '../empleado';
import { EmpleadoService } from '../empleado.service';

@Component({
  selector: 'app-empleado-list',
  templateUrl: './empleado-list.component.html',
  styleUrls: ['./empleado-list.component.css']
})
export class EmpleadoListComponent implements OnInit {
  empleados: Empleado[] = [];
  isLoading: boolean = false;
  errorMessage: string = '';
  
  // Paginación
  currentPage: number = 1;
  itemsPerPage: number = 10;
  totalPages: number = 0;
  totalEmployees: number = 0;
  hasNext: boolean = false;
  hasPrev: boolean = false;

  constructor(
    private empleadoService: EmpleadoService, 
    private router: Router
  ) { }

  ngOnInit() {
    this.loadEmpleados();
  }

  loadEmpleados(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.empleadoService.getEmpleados(this.currentPage, this.itemsPerPage)
      .subscribe({
        next: (response: EmployeeListResponse) => {
          this.empleados = response.employees;
          this.currentPage = response.pagination.page;
          this.totalPages = response.pagination.pages;
          this.totalEmployees = response.pagination.total;
          this.hasNext = response.pagination.has_next;
          this.hasPrev = response.pagination.has_prev;
          this.isLoading = false;
        },
        error: (error) => {
          this.errorMessage = error.message;
          this.isLoading = false;
        }
      });
  }

  // Navegación de páginas
  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages && page !== this.currentPage) {
      this.currentPage = page;
      this.loadEmpleados();
    }
  }

  nextPage(): void {
    if (this.hasNext) {
      this.goToPage(this.currentPage + 1);
    }
  }

  prevPage(): void {
    if (this.hasPrev) {
      this.goToPage(this.currentPage - 1);
    }
  }

  // Acciones de empleados
  eliminarEmpleado(rut: string): void {
    if (confirm('¿Está seguro de que desea eliminar este empleado?')) {
      this.empleadoService.eliminarEmpleado(rut).subscribe({
        next: (response) => {
          alert('Empleado eliminado exitosamente');
          this.loadEmpleados(); // Recargar lista
        },
        error: (error) => {
          alert('Error al eliminar empleado: ' + error.message);
        }
      });
    }
  }

  activarEmpleado(rut: string): void {
    this.empleadoService.activarEmpleado(rut).subscribe({
      next: () => {
        this.loadEmpleados(); // Recargar lista
      },
      error: (error) => {
        alert('Error al activar empleado: ' + error.message);
      }
    });
  }

  volverMenu(): void {
    this.router.navigate(['/']);
  }

  // Helpers
  get pageNumbers(): number[] {
    const pages: number[] = [];
    const start = Math.max(1, this.currentPage - 2);
    const end = Math.min(this.totalPages, this.currentPage + 2);
    
    for (let i = start; i <= end; i++) {
      pages.push(i);
    }
    return pages;
  }

  volverCrear(): void {
    this.router.navigate(['/empleados/crear']);
  }
}