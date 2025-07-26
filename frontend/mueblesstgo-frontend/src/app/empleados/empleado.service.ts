import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { Empleado, EmpleadoRequest, ApiResponse, EmployeeListResponse } from './empleado';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root'
})
export class EmpleadoService {
  private readonly apiUrl = environment.apiUrls.employeeService;

  constructor(private http: HttpClient) { }

  /**
   * Obtener todos los empleados con paginación
   */
  getEmpleados(page: number = 1, perPage: number = 50, activeOnly: boolean = true): Observable<EmployeeListResponse> {
    let params = new HttpParams()
      .set('page', page.toString())
      .set('per_page', perPage.toString())
      .set('active_only', activeOnly.toString());

    return this.http.get<ApiResponse<EmployeeListResponse>>(`${this.apiUrl}/employees`, { params })
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error(response.error || 'Error desconocido');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Crear un nuevo empleado
   */
  crearEmpleado(empleado: EmpleadoRequest): Observable<Empleado> {
    // Convertir fechas al formato esperado por el backend (yyyy/MM/dd)
    const empleadoFormatted = {
      ...empleado,
      fecha_nacimiento: this.formatDateForBackend(empleado.fecha_nacimiento),
      fecha_ingreso: this.formatDateForBackend(empleado.fecha_ingreso)
    };

    return this.http.post<ApiResponse<Empleado>>(`${this.apiUrl}/employees`, empleadoFormatted)
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error(response.error || 'Error al crear empleado');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Obtener un empleado por RUT
   */
  getEmpleadoPorRut(rut: string): Observable<Empleado> {
    return this.http.get<ApiResponse<Empleado>>(`${this.apiUrl}/employees/${rut}`)
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error(response.error || 'Empleado no encontrado');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Actualizar un empleado
   */
  actualizarEmpleado(rut: string, datosActualizacion: Partial<EmpleadoRequest>): Observable<Empleado> {
    // Convertir fechas al formato esperado por el backend si están presentes
    const datosFormatted = { ...datosActualizacion };
    if (datosFormatted.fecha_nacimiento) {
      datosFormatted.fecha_nacimiento = this.formatDateForBackend(datosFormatted.fecha_nacimiento);
    }
    if (datosFormatted.fecha_ingreso) {
      datosFormatted.fecha_ingreso = this.formatDateForBackend(datosFormatted.fecha_ingreso);
    }

    return this.http.put<ApiResponse<Empleado>>(`${this.apiUrl}/employees/${rut}`, datosFormatted)
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error(response.error || 'Error al actualizar empleado');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Eliminar empleado (soft delete)
   */
  eliminarEmpleado(rut: string): Observable<{success: boolean, message: string}> {
    return this.http.delete<{success: boolean, message: string}>(`${this.apiUrl}/employees/${rut}`)
      .pipe(
        map(response => {
          if (response.success) {
            return response;
          }
          throw new Error(response.message || 'Error al eliminar empleado');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Buscar empleados por nombre
   */
  buscarEmpleados(nombre: string, page: number = 1, perPage: number = 50): Observable<EmployeeListResponse> {
    let params = new HttpParams()
      .set('name', nombre)
      .set('page', page.toString())
      .set('per_page', perPage.toString());

    return this.http.get<ApiResponse<EmployeeListResponse>>(`${this.apiUrl}/employees/search`, { params })
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error(response.error || 'Error en la búsqueda');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Obtener empleados por categoría
   */
  getEmpleadosPorCategoria(categoria: 'A' | 'B' | 'C', activeOnly: boolean = true): Observable<Empleado[]> {
    let params = new HttpParams()
      .set('active_only', activeOnly.toString());

    return this.http.get<ApiResponse<Empleado[]>>(`${this.apiUrl}/employees/category/${categoria}`, { params })
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error(response.error || 'Error al obtener empleados por categoría');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Obtener estadísticas de empleados
   */
  getEstadisticas(): Observable<any> {
    return this.http.get<ApiResponse<any>>(`${this.apiUrl}/employees/stats`)
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error(response.error || 'Error al obtener estadísticas');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Activar empleado
   */
  activarEmpleado(rut: string): Observable<Empleado> {
    return this.http.patch<ApiResponse<Empleado>>(`${this.apiUrl}/employees/${rut}/activate`, {})
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error(response.error || 'Error al activar empleado');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Formatea fecha del formato yyyy-MM-dd al formato yyyy/MM/dd esperado por el backend
   */
  private formatDateForBackend(dateString: string): string {
    if (!dateString) return dateString;
    
    // Si ya está en formato yyyy/MM/dd, no hacer nada
    if (dateString.includes('/')) {
      return dateString;
    }
    
    // Convertir de yyyy-MM-dd a yyyy/MM/dd
    return dateString.replace(/-/g, '/');
  }

  /**
   * Manejo de errores HTTP
   */
  private handleError(error: HttpErrorResponse): Observable<never> {
    let errorMessage = 'Ha ocurrido un error desconocido';
    
    if (error.error instanceof ErrorEvent) {
      // Error del lado del cliente
      errorMessage = `Error: ${error.error.message}`;
    } else {
      // Error del lado del servidor
      if (error.error && error.error.error) {
        errorMessage = error.error.error;
      } else if (error.status === 0) {
        errorMessage = 'No se puede conectar al servidor. Verifique su conexión.';
      } else if (error.status === 404) {
        errorMessage = 'Recurso no encontrado';
      } else if (error.status === 409) {
        errorMessage = 'El empleado ya existe';
      } else if (error.status >= 500) {
        errorMessage = 'Error interno del servidor';
      } else {
        errorMessage = `Error ${error.status}: ${error.message}`;
      }
    }
    
    console.error('Error en EmpleadoService:', error);
    return throwError(() => new Error(errorMessage));
  }
}