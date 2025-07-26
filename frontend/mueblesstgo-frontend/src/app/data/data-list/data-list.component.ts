import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { DataUploadService, DataRecord } from '../data-upload.service';

@Component({
  selector: 'app-data-list',
  templateUrl: './data-list.component.html',
  styleUrls: ['./data-list.component.css']
})
export class DataListComponent implements OnInit {
  allData: DataRecord[] = [];
  isLoading: boolean = false;
  errorMessage: string = '';
  
  // Paginación
  currentPage: number = 1;
  itemsPerPage: number = 20;
  totalItems: number = 0;

  constructor(
    private dataUploadService: DataUploadService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.loadAllData();
  }

  loadAllData(): void {
    this.isLoading = true;
    this.errorMessage = '';

    this.dataUploadService.getData().subscribe({
      next: (data: DataRecord[]) => {
        this.allData = data;
        this.totalItems = data.length;
        this.currentPage = 1;
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = error.message;
        this.isLoading = false;
      }
    });
  }

  // Paginación
  get paginatedData(): DataRecord[] {
    const startIndex = (this.currentPage - 1) * this.itemsPerPage;
    const endIndex = startIndex + this.itemsPerPage;
    return this.allData.slice(startIndex, endIndex);
  }

  get totalPages(): number {
    return Math.ceil(this.totalItems / this.itemsPerPage);
  }

  get pageNumbers(): number[] {
    const pages = [];
    for (let i = 1; i <= this.totalPages; i++) {
      pages.push(i);
    }
    return pages;
  }

  goToPage(page: number): void {
    if (page >= 1 && page <= this.totalPages) {
      this.currentPage = page;
    }
  }

  nextPage(): void {
    if (this.currentPage < this.totalPages) {
      this.currentPage++;
    }
  }

  prevPage(): void {
    if (this.currentPage > 1) {
      this.currentPage--;
    }
  }

  volverMenu(): void {
    this.router.navigate(['/']);
  }

  goToUpload(): void {
    this.router.navigate(['/data-upload']);
  }
}
