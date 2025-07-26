import { Component } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  selector: 'app-data-upload',
  templateUrl: './data-upload.component.html',
  styleUrls: ['./data-upload.component.css']
})
export class DataUploadComponent {
  selectedFile: File | null = null;

  constructor(private router: Router) {}

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    this.selectedFile = file ? file : null;
  }

  onUpload(): void {
    // Aquí iría la lógica para subir el archivo
    if (this.selectedFile) {
      alert('Archivo "' + this.selectedFile.name + '" listo para cargar.');
    } else {
      alert('Seleccione un archivo primero.');
    }
  }

  volverMenu(): void {
    this.router.navigate(['/']);
  }
}
