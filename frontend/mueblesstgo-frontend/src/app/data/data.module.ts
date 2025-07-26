import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { DataUploadComponent } from './data-upload/data-upload.component';
import { DataListComponent } from './data-list/data-list.component';
import { DataUploadService } from './data-upload.service';

@NgModule({
  declarations: [
    DataUploadComponent,
    DataListComponent
  ],
  imports: [
    CommonModule,
    FormsModule
  ],
  providers: [DataUploadService],
  exports: [
    DataUploadComponent,
    DataListComponent
  ]
})
export class DataUploadModule { }
