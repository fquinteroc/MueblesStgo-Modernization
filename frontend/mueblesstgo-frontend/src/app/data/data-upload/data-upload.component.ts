import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { DataUploadService, DataUploadResponse } from '../data-upload.service';

@Component({
  selector: 'app-data-upload',
  templateUrl: './data-upload.component.html',
  styleUrls: ['./data-upload.component.css']
})
export class DataUploadComponent {
  selectedFile: File | null = null;
  isUploading: boolean = false;
  uploadResponse: DataUploadResponse | null = null;
  errorMessage: string = '';

  constructor(
    private router: Router,
    private dataUploadService: DataUploadService
  ) {}

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    
    if (file) {
      // Validar que sea un archivo .txt
      if (!file.name.toUpperCase().endsWith('.TXT')) {
        this.errorMessage = 'Por favor seleccione un archivo .TXT';
        this.selectedFile = null;
        return;
      }
      
      // Validar que el nombre sea DATA.TXT
      if (file.name.toUpperCase() !== 'DATA.TXT') {
        this.errorMessage = 'El archivo debe llamarse exactamente "DATA.TXT"';
        this.selectedFile = null;
        return;
      }
      
      this.selectedFile = file;
      this.errorMessage = '';
      this.uploadResponse = null;
    } else {
      this.selectedFile = null;
    }
  }

  onUpload(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Seleccione un archivo primero.';
      return;
    }

    this.isUploading = true;
    this.errorMessage = '';
    this.uploadResponse = null;

    this.dataUploadService.uploadFile(this.selectedFile).subscribe({
      next: (response) => {
        this.uploadResponse = response;
        this.isUploading = false;
        
        if (response.success) {
          // Resetear el input file
          const fileInput = document.getElementById('fileInput') as HTMLInputElement;
          if (fileInput) {
            fileInput.value = '';
          }
          this.selectedFile = null;
        }
      },
      error: (error) => {
        this.errorMessage = error.message;
        this.isUploading = false;
      }
    });
  }

  volverMenu(): void {
    this.router.navigate(['/']);
  }

  goToDataList(): void {
    this.router.navigate(['/data-list']);
  }

  // Getters para el template
  get hasSuccessResponse(): boolean {
    return this.uploadResponse?.success === true;
  }

  get hasErrorResponse(): boolean {
    return this.uploadResponse?.success === false;
  }

  get canUpload(): boolean {
    return this.selectedFile !== null && !this.isUploading;
  }
}
