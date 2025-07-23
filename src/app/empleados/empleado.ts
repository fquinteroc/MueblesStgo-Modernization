export class Empleado {
  id:number;
  rut: string;
  apellidos: string;
  nombres: string;
  fecha_nacimiento: string;
  categoria: string;
  fecha_ingreso: string;
  constructor(
    id: number,
    rut: string,
    apellidos: string,
    nombres: string,
    fecha_nacimiento: string,
    categoria: string,
    fecha_ingreso: string
  ) 
  {
    this.id = id;
    this.rut = rut;
    this.apellidos = apellidos;
    this.nombres = nombres;
    this.fecha_nacimiento = fecha_nacimiento;
    this.categoria = categoria;
    this.fecha_ingreso = fecha_ingreso;
  }
}