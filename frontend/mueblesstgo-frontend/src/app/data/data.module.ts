import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DataUploadComponent } from './data-upload/data-upload.component';

@NgModule({
  declarations: [DataUploadComponent],
  imports: [CommonModule],
  exports: [DataUploadComponent]
})
export class DataUploadModule {}
