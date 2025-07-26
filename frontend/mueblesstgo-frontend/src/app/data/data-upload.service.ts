import { Injectable } from '@angular/core';
import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';
import { environment } from '../../environments/environment';

export interface DataRecord {
  rut: string;
  fecha: string;
  hora: string;
  fecha_creacion?: string;
}

export interface DataUploadResponse {
  success: boolean;
  message: string;
  total_records?: number;
  valid_records?: number;
  invalid_records?: number;
  errors?: string[];
  data?: DataRecord[];
}

export interface DataStats {
  total_records: number;
  unique_ruts: number;
  date_range: {
    earliest: string;
    latest: string;
  };
  records_per_rut: Record<string, number>;
}

@Injectable({
  providedIn: 'root'
})
export class DataUploadService {
  private readonly apiUrl = environment.apiUrls.dataUploadService;

  constructor(private http: HttpClient) { }

  /**
   * Subir archivo DATA.TXT
   */
  uploadFile(file: File): Observable<DataUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post<DataUploadResponse>(`${this.apiUrl}/upload`, formData)
      .pipe(
        catchError(this.handleError)
      );
  }

  /**
   * Obtener todos los datos cargados
   */
  getData(): Observable<DataRecord[]> {
    return this.http.get<{success: boolean, data: DataRecord[]}>(`${this.apiUrl}/data`)
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error('Error al obtener datos');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Obtener datos por RUT específico
   */
  getDataByRut(rut: string): Observable<DataRecord[]> {
    return this.http.get<{success: boolean, data: DataRecord[]}>(`${this.apiUrl}/data/rut/${rut}`)
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error('Error al obtener datos por RUT');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Obtener lista de RUTs únicos
   */
  getDistinctRuts(): Observable<string[]> {
    return this.http.get<{success: boolean, data: string[]}>(`${this.apiUrl}/ruts`)
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error('Error al obtener RUTs');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Obtener estadísticas de los datos
   */
  getStats(): Observable<DataStats> {
    return this.http.get<{success: boolean, data: DataStats}>(`${this.apiUrl}/stats`)
      .pipe(
        map(response => {
          if (response.success && response.data) {
            return response.data;
          }
          throw new Error('Error al obtener estadísticas');
        }),
        catchError(this.handleError)
      );
  }

  /**
   * Verificar el estado del servicio
   */
  ping(): Observable<{status: string, service: string}> {
    return this.http.get<{status: string, service: string}>(`${this.apiUrl}/ping`)
      .pipe(
        catchError(this.handleError)
      );
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
      } else if (error.status === 400) {
        errorMessage = 'Archivo inválido o datos incorrectos';
      } else if (error.status === 404) {
        errorMessage = 'Recurso no encontrado';
      } else if (error.status >= 500) {
        errorMessage = 'Error interno del servidor';
      } else {
        errorMessage = `Error ${error.status}: ${error.message}`;
      }
    }
    
    console.error('Error en DataUploadService:', error);
    return throwError(() => new Error(errorMessage));
  }
}
