import { Component, Input, Output, EventEmitter } from '@angular/core';
import {FormBuilder, FormGroup, FormsModule, ReactiveFormsModule, Validators} from '@angular/forms';
import { HttpService } from '../services/http.service';
import {NgForOf, NgIf} from '@angular/common';
import {List} from '../models/list';
import {HttpErrorResponse} from '@angular/common/http';

@Component({
  selector: 'app-create-card-form',
  standalone: true,
  imports: [
    NgIf,
    FormsModule,
    ReactiveFormsModule,
    NgForOf
  ],
  templateUrl: './create-card-form.component.html',
  styleUrl: './create-card-form.component.css'
})
export class CreateCardFormComponent {
  @Input() list: List | undefined;
  @Output() closeModal: EventEmitter<void> = new EventEmitter<void>();
  @Output() refresh: EventEmitter<void> = new EventEmitter<void>();

  priorities: string[] = ["Low", "Medium", "High"];
  statuses: string[] = ["ToDo", "InProcess", "Done", "Backlog", "Blocked"];

  cardForm: FormGroup;

  constructor(private httpService: HttpService, private fb: FormBuilder) {
    this.cardForm = this.fb.group({
      title: ['', Validators.required],
      description: ['', Validators.required],
    });
  }

  onSubmit(): void {
    if (this.list !== undefined && this.list.idList) {
      this.httpService.postCard(
        this.cardForm.value.description,
        this.list.idList,
        this.cardForm.value.title
      ).subscribe(
        (response: any): void => {
          this.close();
          this.refresh.emit();
        }, (err: HttpErrorResponse): void => {
          console.log(err);
        }
      );
    }
  }

  close(): void {
    this.closeModal.emit();
  }

  generateCardDescription(): void {
    this.httpService.generateCardDescription(
      this.cardForm.value.title,
    ).subscribe(
      (response: string): void => {
        this.cardForm.patchValue({
          description: response,
        });
      }, (err: HttpErrorResponse): void => {
        console.log(err);
      }
    );
  }
}
