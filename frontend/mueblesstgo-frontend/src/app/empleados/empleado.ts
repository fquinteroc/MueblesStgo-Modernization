export interface Empleado {
  rut: string;
  apellidos: string;
  nombres: string;
  fecha_nacimiento: string;
  categoria: 'A' | 'B' | 'C';
  fecha_ingreso: string;
  activo?: boolean;
  fecha_creacion?: string;
  fecha_actualizacion?: string;
}

export interface EmpleadoRequest {
  rut: string;
  apellidos: string;
  nombres: string;
  fecha_nacimiento: string;
  categoria: 'A' | 'B' | 'C';
  fecha_ingreso: string;
}

export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
  error?: string;
}

export interface EmployeeListResponse {
  employees: Empleado[];
  pagination: {
    page: number;
    per_page: number;
    total: number;
    pages: number;
    has_next: boolean;
    has_prev: boolean;
  };
}